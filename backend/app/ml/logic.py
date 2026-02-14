import os.path
import pandas
import spacy
import re
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# --- SETUP NLP ---
nlp = spacy.load("en_core_web_sm")
custom_stop_words = [
    # Hiring / Generic
    "job", "description", "role", "seek", "position", "candidate", "ideal",
    "opportunity", "join", "client", "company", "new", "type", "remote",
    "experience", "work", "year", "skill", "require", "requirement", "include",
    "need", "strong", "ability", "knowledge", "responsible",

    # HR / Benefits
    "pay", "benefit", "salary", "range", "employee", "disability", "equal",
    "time", "base", "status",

    # Vague Verbs
    "provide", "focus", "drive", "collaborate", "support", "build", "help",
    "create", "maintain", "perform",

    # Generic Tech Context (Too broad to be useful)
    "solution", "system", "environment", "platform", "product", "service",
    "technology", "technical", "application", "industry", "high", "software",
    "engineer", "engineering", "development", "develop",

    # NEW: Recruiting & Process
    "interview", "recruiter", "prospect", "candidate", "select", "review",
    "meet", "touch", "region", "status", "fill", "join", "process", "aspect",

    # NEW: Corporate Fluff & Adjectives
    "impact", "fast", "pace", "inspire", "excite", "excited", "successful",
    "dynamic", "demanding", "challenge", "varied", "culture", "passion",
    "mission", "critical", "commercial", "good", "excellent", "solid",
    "expert", "proficiently", "minimum", "related", "specific", "wide",
    "array", "proven", "track", "record", "strong", "deep", "outcome",
    "real", "thinker", "acuman", "acumen", "important", "fundamental",

    # NEW: Benefits & Legal
    "insurance", "medical", "life", "retirement", "tax", "free", "saving",
    "plan", "healthcare", "incentive", "compensation", "eligible",
    "discretionary", "bonus", "bachelor", "degree", "discipline", "stem",
    "accordance", "applicable", "law", "legal", "compliance", "regulatory",
    "addition", "program", "fund", "funding", "settlement", "investor",

    # NEW: Generic Verbs/Nouns
    "look", "know", "prove", "manage", "solve", "participate", "align",
    "increase", "maximize", "iterate", "define", "spec", "change", "flex",
    "course", "pre", "gen", "desk", "partner", "team", "task", "problem",
    "dissect", "return", "efficiency", "research", "analysis", "power",

    # Generic Nouns
    "skill", "skills", "talent", "level", "following", "access",
    "aspect", "impact", "prospect", "outcome", "change", "course",
    "desk", "gen", "spec", "pre", "market", "interview", "seniority",

    "https", "http", "com", "www", "career", "careers", "apply",
    "website", "location", "locations", "email", "contact",
    "toast", "toasttab", "restaurant"
]

# Update Spacy's default stop words
for word in custom_stop_words:
    lex = nlp.vocab[word]
    lex.is_stop = True

# --- CLEANING FUNCTION ---
def clean_text(text):
    """
    Function to return cleaned token using nlp
    :param text: str
    :return: object
    """

    text = text.lower()

    # Remove URLs (http/https/www)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)

    # 3. Remove Email Addresses
    text = re.sub(r'\S+@\S+', '', text)

    doc = nlp(text)

    allowed_pos = ["NOUN", "PROPN"]
    clean_tokens = []

    for token in doc:
        lemma = token.lemma_.lower()

        if(
            not token.is_stop
            and not token.is_punct
            and not token.like_num
            and token.pos_ in allowed_pos
            and lemma not in custom_stop_words
            and len(lemma) > 2
        ):
            clean_tokens.append(lemma)

    return " ".join(clean_tokens)

# ---- THE MATCHER -----
class JobMatcher:
    """
    Class to implement the job matching logic
    """

    def __init__(self):
        # Load the model only when the class is initialized
        self.tfidf: TfidfVectorizer
        self.df: pandas.DataFrame
        model_path = os.path.join(os.path.dirname("./"), "model.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model artifact not found at {model_path}. Run train.py first.")

        with open(model_path, "rb") as fd:
            self.tfidf, self.tfidf_matrix, self.df = pickle.load(fd)

        # Get the vocabulary
        self.feature_names = np.array(self.tfidf.get_feature_names_out())

    @staticmethod
    def combine_user_fields(user_profile:dict) -> str:
        """
        Helper function to merge structured user fields into a single text
        blocks.
        Args:
            user_profile: dict

        Returns: str
        """
        fields = [
            user_profile.get("target_roles", ""),
            user_profile.get("skills", ""),
            user_profile.get("experience_level", "")
        ]

        results = []
        for f in fields:
            if isinstance(f, list):
                for item in f:
                    results.append(str(item))
            else:
                results.append(str(f))

        return " ".join(results)

    def get_missing_skills(self, user_vector, job_idx):
        """
        Identifies high value keywords present in the Job but missing from the
        User Vector
        Args:
            user_vector: ndarray array of shape
            job_idx: int

        Returns: list
        """

        # Get the vector for the specific job
        job_vector = self.tfidf_matrix[job_idx].toarray().flatten()
        user_vector_dense = user_vector.toarray().flatten()

        # Find indices where Job > 0 but the User == 0
        missing_indices = np.where((job_vector > 0) & (user_vector_dense == 0))[0]

        # Sort the importance
        # We want the heaviest missing words, not just any missing word.
        # Sort indices by job_vector weight descending.
        sorted_missing = sorted(missing_indices, key=lambda i: job_vector[
            i], reverse=True)

        # Convert top 5 indices back to words
        top_missing_words = self.feature_names[sorted_missing[:5]].tolist()

        return top_missing_words

    def recommend(self, user_profile:dict, top_n=10):
        """
        Class method to implement cosine similarity logic to compare the
        "User Vector" against the "Job Vectors" and output a raw match score
        Args:
            user_profile: dict
            top_n: int

        Returns: dict
        """

        # Pre-processing
        user_text = self.combine_user_fields(user_profile)

        # Clean the User Input
        cleaned_text = clean_text(user_text)

        # Convert the User Input to Numbers (Vector)
        user_vector = self.tfidf.transform([cleaned_text])

        # Calculate the cosine similarity
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()

        # Get Top N Matches
        top_indices = similarities.argsort()[-top_n:][::-1]

        # Format Results
        results = []
        for index in top_indices:
            score = similarities[index]

            # Filter: Only return if there is some relevancy
            if score < 0.05:
                continue

            job_row = self.df.iloc[index]

            # Find missing skills
            missing = self.get_missing_skills(user_vector, index)

            results.append({
                "job_id": str(job_row.get("_id")),
                "title": job_row.get("title", "Unknown"),
                "company": job_row.get("company", "Unknown"),
                "score": round(score, 2),
                "missing_skill": missing
            })

        return results
