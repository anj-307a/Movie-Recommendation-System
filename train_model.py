from core.data_preprocessing import DataPreprocessor
from core.feature_engineering import FeatureEngineer
from core.model_builder import ModelBuilder

print("Starting preprocessing...")

preprocessor = DataPreprocessor()
df = preprocessor.preprocess()

engineer = FeatureEngineer(df)
df = engineer.build_weighted_features()

builder = ModelBuilder(df)
builder.build()

print("Model built successfully!")