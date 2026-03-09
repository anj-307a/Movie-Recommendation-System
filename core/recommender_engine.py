import pickle
import numpy as np
import difflib
import random
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from core.config import Config
from core.logger import get_logger

logger = get_logger(__name__)


class CineMatchEngine:

    def __init__(self):
        logger.info("Initializing CineMatchEngine")

        self.similarity = pickle.load(open(Config.SIMILARITY_FILE, "rb"))
        self.df = pickle.load(open(Config.MOVIES_CLEAN_FILE, "rb"))

        self.indices = pd.Series(self.df.index, index=self.df["title"]).to_dict()
        self.scaler = MinMaxScaler()

        logger.info("Engine loaded successfully")

    def find_closest_title(self, title):
        matches = difflib.get_close_matches(title, self.indices.keys(), n=1, cutoff=0.6)
        return matches[0] if matches else None

    def surprise_me(self):
        return self.df.sample(1).iloc[0].title

    def recommend(self, title, top_k=10, min_rating=0, genre_filter=None):

        if title not in self.indices:
            suggestion = self.find_closest_title(title)
            return {
                "error": f"Movie not found. Did you mean '{suggestion}'?"
            }

        idx = self.indices[title]
        sim_scores = self.similarity[idx].toarray().flatten()

        sim_scores = self.scaler.fit_transform(
            sim_scores.reshape(-1, 1)
        ).flatten()

        rating_scores = self.scaler.fit_transform(
            self.df["vote_average"].values.reshape(-1, 1)
        ).flatten()

        popularity_scores = self.scaler.fit_transform(
            self.df["popularity"].values.reshape(-1, 1)
        ).flatten()

        final_score = (
            0.65 * sim_scores +
            0.25 * rating_scores +
            0.10 * popularity_scores
        )

        scored_movies = list(enumerate(final_score))
        scored_movies = sorted(scored_movies, key=lambda x: x[1], reverse=True)

        results = []

        for i, score in scored_movies[1:]:

            movie = self.df.iloc[i]

            if movie.vote_average < min_rating:
                continue

            if genre_filter:
                if genre_filter.lower() not in movie.genres:
                    continue

            results.append({
                "title": movie.title,
                "confidence": round(score * 100, 2),
                "rating": movie.vote_average,
                "genres": movie.genres,
                "popularity": movie.popularity
            })

            if len(results) == top_k:
                break

        return results