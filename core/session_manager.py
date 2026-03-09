import streamlit as st
from core.logger import get_logger

logger = get_logger(__name__)


class SessionManager:
    """
    Manages session-based user history
    """

    @staticmethod
    def initialize():
        if "history" not in st.session_state:
            st.session_state.history = []
            logger.info("Session history initialized")

    @staticmethod
    def add_to_history(movie_title: str):
        if movie_title not in st.session_state.history:
            st.session_state.history.append(movie_title)
            logger.info(f"Added '{movie_title}' to session history")

    @staticmethod
    def get_history():
        return st.session_state.history

    @staticmethod
    def clear_history():
        st.session_state.history = []
        logger.info("Session history cleared")