import matplotlib.pyplot as plt
import numpy as np
from core.logger import get_logger

logger = get_logger(__name__)


class VisualizationEngine:

    @staticmethod
    def plot_similarity_heatmap(sim_matrix, indices, movie_title):
        """
        Plot similarity heatmap of top 5 similar movies
        """

        logger.info(f"Generating similarity heatmap for {movie_title}")

        idx = indices.get(movie_title)

        if idx is None:
            logger.warning("Movie not found in indices")
            return None

        scores = sim_matrix[idx].toarray().flatten()

        # Get top 6 including itself
        top_indices = scores.argsort()[-6:][::-1]

        heatmap_matrix = sim_matrix[top_indices][:, top_indices].toarray()

        fig, ax = plt.subplots(figsize=(6, 5))

        cax = ax.imshow(heatmap_matrix)

        ax.set_title("Top 5 Similarity Heatmap")
        fig.colorbar(cax)

        plt.tight_layout()

        return fig