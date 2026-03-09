import numpy as np


class Evaluator:

    @staticmethod
    def precision_at_k(recommended, relevant, k=10):
        recommended_k = recommended[:k]
        relevant_set = set(relevant)

        relevant_count = sum(
            1 for movie in recommended_k
            if movie in relevant_set
        )

        return relevant_count / k