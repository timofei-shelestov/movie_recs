import numpy as np


class GenreVectorizer:
  def __init__(self):
    self.genre_to_index = {}
    self.n_genres = 0

  def fit(self, movies):
    count = 0

    for movie in movies:
      genre_ids = set(int(x) for x in movie["genre_ids"].split(","))
      for genre_id in genre_ids:
        if genre_id not in self.genre_to_index:
          self.genre_to_index[genre_id] = count
          count = count + 1

  def transform(self, movies):
    feature_mtx = np.zeros((len(movies), len(self.genre_to_index)), dtype=np.uint32)
    
    for movie_idx, movie in enumerate(movies):  
      genre_ids = set(int(x) for x in movie["genre_ids"].split(","))
      for genre_id in genre_ids:
        feature_mtx[movie_idx, self.genre_to_index[genre_id]] = 1
        

    return feature_mtx

  def _vectorize_single_movie(self, movie):
    genre_ids = set(int(x) for x in movie["genre_ids"].split(","))
    vec = np.zeros((1, len(self.genre_to_index)), dtype=np.uint32)

    for genre_id in genre_ids:
      vec[0, self.genre_to_index[genre_id]] = 1

    return vec
