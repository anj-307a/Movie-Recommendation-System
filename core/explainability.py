import pickle
from core.config import Config


class ExplainabilityEngine:

    def __init__(self):
        self.df = pickle.load(open(Config.MOVIES_CLEAN_FILE, "rb"))

    def explain(self, movie1, movie2):

        row1 = self.df[self.df["title"] == movie1].iloc[0]
        row2 = self.df[self.df["title"] == movie2].iloc[0]

        common_genres = set(row1["genres"]) & set(row2["genres"])
        common_keywords = set(row1["keywords"]) & set(row2["keywords"])

        explanation = (
            f"Recommended because it shares "
            f"{', '.join(list(common_genres)[:2])} "
            f"themes with {movie1}."
        )

        return {
            "common_genres": list(common_genres),
            "common_keywords": list(common_keywords)[:5],
            "reason": explanation
        }