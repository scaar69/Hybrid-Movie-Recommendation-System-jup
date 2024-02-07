import requests
import pandas as pd

# set up API key
api_key = 'e0cf92b5d30420088a5a3a0da49dac81'

# function to make requests to TMDB API
def get_movie_details(title, year, genre):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': title, 'year': year, 'with_genres': genre}
    response = requests.get(url, params=params)
    data = response.json()
    return data

# make a request for popular movies
url = 'https://api.themoviedb.org/3/movie/popular'
params = {'api_key': api_key}
response = requests.get(url, params=params)
data = response.json()

# create a pandas dataframe from the movie data
movies = pd.DataFrame(data['results'])

# preprocess the data by dropping duplicates and missing values
movies.drop_duplicates(subset='id', inplace=True)
movies.dropna(inplace=True)

# content-based filtering
# create a new dataframe with relevant movie features
features = ['id', 'title', 'genres', 'keywords', 'cast', 'crew']
movies_features = movies[features].copy()

# convert genre, cast, and keyword columns to lists
movies_features['genres'] = movies_features['genres'].apply(lambda x: [genre['name'] for genre in x])
movies_features['keywords'] = movies_features['keywords'].apply(lambda x: [keyword['name'] for keyword in x])
movies_features['cast'] = movies_features['cast'].apply(lambda x: [cast['name'] for cast in x])

# create a new column with combined features
movies_features['combined_features'] = movies_features.apply(lambda row: ' '.join(row['genres']) + ' ' + ' '.join(row['keywords']) + ' ' + ' '.join(row['cast']), axis=1)

# create a CountVectorizer to convert the combined features into a matrix of token counts
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
count_matrix = cv.fit_transform(movies_features['combined_features'])

# calculate the cosine similarity between each pair of movies
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(count_matrix)

# collaborative filtering
# create a ratings matrix by pivoting the ratings data
ratings = pd.read_csv('ratings.csv')
ratings_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')

# create a function to get the top N recommendations for a user
def get_top_n_recommendations(userId, n):
    # get the user's ratings
    user_ratings = ratings_matrix.loc[userId].dropna()
    # calculate the cosine similarity between the user's ratings and all other ratings
    sim_scores = ratings_matrix.dropna(axis=1).apply(lambda x: cosine_similarity([user_ratings, x])[0,1], axis=0)
    # sort the movies by similarity score and return the top N recommendations
    movie_indices = sim_scores.sort_values(ascending=False)[:n].index
    return movies[movies['id'].isin(movie_indices)]['title']

# test the recommendation system
print(get_top_n_recommendations(1, 10))
