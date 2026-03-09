class FeatureEngineer:

    def __init__(self, df):
        self.df = df

    def build_weighted_features(self):
        """
        Unique Enhancement:
        Apply weighted repetition to important features.
        """
        def combine(row):
            overview = row["overview"]
            genres = " ".join(row["genres"]) * 3
            keywords = " ".join(row["keywords"]) * 2
            cast = " ".join(row["cast"]) * 1
            director = row["director"] * 3

            return f"{overview} {genres} {keywords} {cast} {director}"

        self.df["combined"] = self.df.apply(combine, axis=1)
        return self.df