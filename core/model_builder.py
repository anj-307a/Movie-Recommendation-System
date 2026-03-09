import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.config import Config
from core.logger import get_logger

logger = get_logger(__name__)

class ModelBuilder:

    def __init__(self, df):
        self.df = df

    def build(self):

        logger.info("Building TF-IDF vectorizer")

        tfidf = TfidfVectorizer(
            max_features=Config.MAX_FEATURES,
            stop_words="english",
            ngram_range=Config.NGRAM_RANGE,
            sublinear_tf=True
        )

        vectors = tfidf.fit_transform(self.df["combined"])

        logger.info("Computing cosine similarity matrix")
        similarity = cosine_similarity(vectors, dense_output=False)

        os.makedirs(Config.MODEL_PATH, exist_ok=True)

        pickle.dump(similarity, open(Config.SIMILARITY_FILE, "wb"))
        pickle.dump(tfidf, open(Config.TFIDF_FILE, "wb"))
        pickle.dump(self.df, open(Config.MOVIES_CLEAN_FILE, "wb"))

        logger.info("Model artifacts saved successfully")