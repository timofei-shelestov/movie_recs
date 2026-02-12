import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import cos_similarity


class ContentRecommender():
  def __init__(self, GenreVectorizer, TfidfVectorizer):
    self.genre_vectorizer = GenreVectorizer()
    self.tfidf_vectorizer = TfidfVectorizer()
    self.movie_vecs = np.empty([])
    self.movie_id_to_index = {}
    self.movies = {}
  
  def fit(self, movies):
    self.genre_vectorizer.fit(movies)
    self.tfidf_vectorizer.fit(movies)
   

    self.movie_id_to_index = {
      movie['id']: idx
      for idx, movie in enumerate(movies)
    }

    genre_vec = self.genre_vectorizer.transform(movies)
    tfidf_vec = self.tfidf_vectorizer.transform(movies)

    self.movie_vecs = np.column_stack((genre_vec * 5, tfidf_vec))
    self.movies = movies  

    
  def find_similiar(self, movie_id, n): 
    target_idx = self.movie_id_to_index[movie_id]
    target_vec  = self.movie_vecs[target_idx]

    similarity_vec = cosine_similarity([target_vec], self.movie_vecs)[0]
    
    sorted_idx = np.argsort(similarity_vec)[::-1][1:n+1]
    results = []

    for idx in sorted_idx:
      movie = self.movies[idx]
      score = similarity_vec[idx]

      results.append({
        "movie_id": movie["id"],
        "title": movie["title"],
        "score": score, 
      })
    
    return results 
 