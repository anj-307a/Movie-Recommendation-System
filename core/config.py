import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DATA_PATH = os.path.join(BASE_DIR, "data")
    MODEL_PATH = os.path.join(BASE_DIR, "models")

    MOVIES_FILE = os.path.join(DATA_PATH, "tmdb_5000_movies.csv")
    CREDITS_FILE = os.path.join(DATA_PATH, "tmdb_5000_credits.csv")

    SIMILARITY_FILE = os.path.join(MODEL_PATH, "similarity.pkl")
    TFIDF_FILE = os.path.join(MODEL_PATH, "tfidf_vectorizer.pkl")
    MOVIES_CLEAN_FILE = os.path.join(MODEL_PATH, "movies_clean.pkl")

    MAX_FEATURES = 8000
    NGRAM_RANGE = (1, 2)