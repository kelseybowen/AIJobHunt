import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from logic import clean_text

def build_model():
    """
    Docstring for build_model
    """

    # Load Data
    df = pd.read_csv('data/adzuna_top25_20260123_20_17_49.csv')

    # Clean Data
    df['processed_text'] = df['Description'].apply(clean_text)

    # Perform TD-IDF Vectorizer
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.85,
        sublinear_tf=True
    )

    # Fit the model
    tfidf_matrix = tfidf.fit_transform(df['processed_text'])

    # Save the model
    print("Saving to model.pkl")
    with open("model.pkl", "wb") as f:
        pickle.dump((tfidf, tfidf_matrix, df), f)

    print("Done!")

if __name__ == "__main__":
    build_model()