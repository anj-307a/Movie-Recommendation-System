import pandas as pd
import ast
import re
from core.config import Config
from core.logger import get_logger

logger = get_logger(__name__)


class DataPreprocessor:

    def __init__(self):
        logger.info("Initializing DataPreprocessor")
        self.movies = pd.read_csv(Config.MOVIES_FILE)
        self.credits = pd.read_csv(Config.CREDITS_FILE)

    # --------------------------------------------------
    # Merge Movies + Credits Dataset
    # --------------------------------------------------

    def merge(self):
        self.credits.rename(columns={"movie_id": "id"}, inplace=True)

        df = self.movies.merge(self.credits, on="id", how="inner")

        # Handle duplicate title columns
        if "title_x" in df.columns:
            df.rename(columns={"title_x": "title"}, inplace=True)

        if "title_y" in df.columns:
            df.drop(columns=["title_y"], inplace=True)

        logger.info("Datasets merged successfully")
        return df

    # --------------------------------------------------
    # JSON Parsing Helper
    # --------------------------------------------------

    @staticmethod
    def parse_json_column(column):
        def safe_parse(x):
            try:
                return ast.literal_eval(x) if pd.notnull(x) else []
            except:
                return []
        return column.apply(safe_parse)

    # --------------------------------------------------
    # Extract Name Fields
    # --------------------------------------------------

    @staticmethod
    def extract_names(items, key="name", limit=None):
        names = []
        for item in items:
            if key in item:
                cleaned = item[key].replace(" ", "").lower()
                names.append(cleaned)

        return names[:limit] if limit else names

    # --------------------------------------------------
    # Extract Director from Crew
    # --------------------------------------------------

    @staticmethod
    def extract_director(crew):
        for member in crew:
            if member.get("job") == "Director":
                return member["name"].replace(" ", "").lower()
        return ""

    # --------------------------------------------------
    # Clean Overview Text
    # --------------------------------------------------

    @staticmethod
    def clean_text(text):
        text = re.sub(r"[^a-zA-Z0-9 ]", " ", str(text))
        return text.lower().strip()

    # --------------------------------------------------
    # Main Preprocessing Pipeline
    # --------------------------------------------------

    def preprocess(self):

        df = self.merge()

        # Check required columns
        required_columns = [
            "id", "title", "overview",
            "genres", "keywords",
            "cast", "crew",
            "vote_average", "popularity"
        ]

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns in dataset: {missing}")

        logger.info("Parsing JSON columns...")

        df["genres"] = self.parse_json_column(df["genres"])
        df["keywords"] = self.parse_json_column(df["keywords"])
        df["cast"] = self.parse_json_column(df["cast"])
        df["crew"] = self.parse_json_column(df["crew"])

        logger.info("Extracting structured features...")

        df["genres"] = df["genres"].apply(
            lambda x: self.extract_names(x)
        )

        df["keywords"] = df["keywords"].apply(
            lambda x: self.extract_names(x)
        )

        df["cast"] = df["cast"].apply(
            lambda x: self.extract_names(x, limit=3)
        )

        df["director"] = df["crew"].apply(
            lambda x: self.extract_director(x)
        )

        df["overview"] = df["overview"].fillna("").apply(self.clean_text)

        # Select only required columns
        df = df[[
            "id",
            "title",
            "overview",
            "genres",
            "keywords",
            "cast",
            "director",
            "vote_average",
            "popularity"
        ]]

        logger.info("Preprocessing completed successfully")
        return df