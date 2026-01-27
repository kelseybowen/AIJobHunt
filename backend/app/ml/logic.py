import spacy
import re
import pickle
import numpy as np

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

    return list(set(clean_tokens))