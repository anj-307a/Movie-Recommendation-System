import sys
import os
# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import time
from core.recommender_engine import CineMatchEngine
from core.session_manager import SessionManager
from core.visualization import VisualizationEngine
from core.api_clients import TMDBClient
from ui.components import UIComponents

# Page Config
st.set_page_config(
    page_title="CineMatch AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open("ui/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Systems
engine = CineMatchEngine()
tmdb = TMDBClient()
SessionManager.initialize()

# Header
UIComponents.glowing_header()

# Sidebar Controls
st.sidebar.title("🎛 Filters")

search_movie = st.sidebar.selectbox(
    "Search Movie",
    engine.df["title"]
)

mood = st.sidebar.selectbox(
    "Select Mood",
    ["None", "Happy", "Romantic", "Action-packed", "Thriller"]
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    0.0, 10.0, 5.0
)

genre_filter = st.sidebar.text_input("Genre Filter")

if st.sidebar.button("🎲 Surprise Me"):
    search_movie = engine.surprise_me()

# Trending Section
trending = tmdb.get_trending()
UIComponents.display_horizontal_trending(trending)

# Recommendation Section
st.subheader("✨ Recommendations")

if st.button("Generate Recommendations"):

    with st.spinner("Analyzing cinematic patterns..."):
        time.sleep(1.5)

        results = engine.recommend(
            search_movie,
            top_k=10,
            min_rating=min_rating,
            genre_filter=genre_filter
        )

        SessionManager.add_to_history(search_movie)

    if "error" in results:
        st.error(results["error"])
    else:
        cols = st.columns(5)
        for i, rec in enumerate(results[:5]):
            with cols[i]:
                UIComponents.display_movie_card(search_movie, rec)

        # Heatmap
        st.subheader("📊 Similarity Analysis")
        fig = VisualizationEngine.plot_similarity_heatmap(
            engine.similarity,
            engine.indices,
            search_movie
        )
        if fig:
            st.pyplot(fig)

# Session History
st.sidebar.subheader("🕘 Session History")
history = SessionManager.get_history()
for movie in history:
    st.sidebar.write(movie)