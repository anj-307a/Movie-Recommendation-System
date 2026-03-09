import streamlit as st
from core.session_manager import SessionManager
from core.explainability import ExplainabilityEngine
from core.api_clients import TMDBClient

tmdb = TMDBClient()
explainer = ExplainabilityEngine()


class UIComponents:

    @staticmethod
    def glowing_header():
        st.markdown(
            '<div class="glow-title">🎬 CineMatch AI</div>',
            unsafe_allow_html=True
        )

    @staticmethod
    def display_movie_card(base_movie, rec):

        poster = tmdb.get_poster_url(rec["title"])

        with st.container():

            st.markdown('<div class="poster">', unsafe_allow_html=True)

            if poster:
                st.image(poster)

            st.markdown(f"### {rec['title']}")
            st.progress(rec["confidence"] / 100)
            st.write(f"⭐ Rating: {rec['rating']}")

            # Simple trailer search link (no API needed)
            trailer_search_link = (
                f"https://www.youtube.com/results?search_query="
                f"{rec['title']}+official+trailer"
            )

            st.link_button("🎥 Watch Trailer", trailer_search_link)

            explanation = explainer.explain(base_movie, rec["title"])

            with st.expander("Why recommended?"):
                st.write("Shared Genres:", explanation["common_genres"])
                st.write("Common Keywords:", explanation["common_keywords"])
                st.info(explanation["reason"])

            st.markdown("</div>", unsafe_allow_html=True)

    @staticmethod
    def display_horizontal_trending(trending_movies):

        st.subheader("🔥 Trending Now")

        cols = st.columns(6)

        for i, movie in enumerate(trending_movies[:6]):
            with cols[i]:
                poster = tmdb.get_poster_url(movie["title"])
                if poster:
                    st.image(poster)
                st.caption(movie["title"])