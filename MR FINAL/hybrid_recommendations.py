import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load movie data from CSV file

df = pd.read_csv('tamil_movies.csv')

# Compute TF-IDF vectors for movie overviews
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Review Data'].values.astype('U'))

# Compute cosine similarity between all pairs of movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Define function to recommend movies based on a given movie title
def hybrid_recommendations(title, num_recommendations=10):
    # Find the index of the movie in the DataFrame
    idx = df.index[df['Title'] == title].tolist()[0]

    # Get the cosine similarity scores for all movies relative to the given movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies by their similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the titles and genres of the top recommended movies
    movie_indices = [i[0] for i in sim_scores[1:]]
    recommended_movies = df.iloc[movie_indices][['Title', 'Genre']].values.tolist()[:num_recommendations]

    # Return the recommended movies
    return recommended_movies

# Test the recommendation system by recommending movies based on the movie "Kaala"
print(hybrid_recommendations("Pathu Thala"))