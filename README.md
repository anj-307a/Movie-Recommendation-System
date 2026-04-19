# Movie Recommendation System

## Overview
This project is a Movie Recommendation System that suggests movies to users based on similarity and user preferences. It uses machine learning techniques to analyze movie data and recommend relevant movies.

## Features
- Search movies easily
- Recommend similar movies
- Machine learning-based recommendations
- Uses NLP techniques for better matching
- Simple UI for user interaction

## Tech Stack
- Language: Python
- Libraries: Pandas, NumPy, Scikit-learn
- Machine Learning: Content-Based Filtering
- Frontend: Basic UI (inside ui/ folder)

## Project Structure
movie-recommendation-system/
│
├── core/               # Core logic
├── data/               # Dataset files
├── logs/               # Log files
├── ui/                 # User interface
├── train_model.py      # Model training
├── requirements.txt    # Dependencies
└── README.md           # Documentation

## How It Works
1. Load dataset from data/
2. Preprocess data (cleaning and feature extraction)
3. Convert text into vectors (TF-IDF / Count Vectorizer)
4. Calculate similarity between movies
5. Recommend top similar movies

## How to Run

### Clone repository
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system

### Install dependencies
pip install -r requirements.txt

### Train model
python train_model.py

### Run application
python app.py

## Dataset
- Movie titles
- Genres
- Keywords
- Ratings

## Algorithms Used
- Content-Based Filtering
- Cosine Similarity
- NLP (Text Vectorization)

## Important Files
- train_model.py → trains the model
- core/ → recommendation logic
- ui/ → user interface

## Future Improvements
- Add user login
- Implement collaborative filtering
- Deploy using AWS or Streamlit
- Improve UI design

## Author
Anjali

## License
This project is for educational purposes only.
