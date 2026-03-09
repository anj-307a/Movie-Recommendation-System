import requests
import streamlit as st
from functools import lru_cache
from core.logger import get_logger

logger = get_logger(__name__)


class TMDBClient:
    """
    Handles TMDB API communication.
    """

    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

    def __init__(self):
        try:
            self.api_key = st.secrets["TMDB_API_KEY"]
        except Exception:
            raise ValueError("TMDB API key not found in Streamlit secrets.")

    # ---------------------------------------------------
    # Fetch Movie By Title
    # ---------------------------------------------------

    @lru_cache(maxsize=500)
    def get_movie_by_title(self, title: str):
        try:
            url = f"{self.BASE_URL}/search/movie"
            params = {
                "api_key": self.api_key,
                "query": title
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data["results"]:
                return data["results"][0]
            return None

        except Exception as e:
            logger.error(f"Error fetching movie: {e}")
            return None

    # ---------------------------------------------------
    # Fetch Poster
    # ---------------------------------------------------

    @lru_cache(maxsize=500)
    def get_poster_url(self, title: str):
        movie = self.get_movie_by_title(title)

        if not movie or not movie.get("poster_path"):
            return None

        return f"{self.IMAGE_BASE}{movie['poster_path']}"

    # ---------------------------------------------------
    # Fetch Trending
    # ---------------------------------------------------

    @lru_cache(maxsize=1)
    def get_trending(self):
        try:
            url = f"{self.BASE_URL}/trending/movie/day"
            params = {"api_key": self.api_key}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return data.get("results", [])

        except Exception as e:
            logger.error(f"Error fetching trending: {e}")
            return []