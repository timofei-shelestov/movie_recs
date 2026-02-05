import numpy as np


class GenreVectorizer:
  def __init__(self):
    self.genre_to_index = {}
    self.n_genres = 0

  def fit(self, movies):
    count = 0

    for movie in movies:
      genre_ids = [int(x) for x in movie["genre_ids"].split(",")]
      for genre_id in genre_ids:
        if genre_id not in self.genre_to_index:
          self.genre_to_index[genre_id] = count
          count = count + 1

  def transform(self, movies):
    feature_vec = []
    for movie in movies:
      temp_vec = []
      genre_ids = [int(x) for x in movie["genre_ids"].split(",")]
      for genre_id in self.genre_to_index:
        if genre_id in genre_ids:
          temp_vec.insert(self.genre_to_index[genre_id], 1)
        else:
          temp_vec.insert(self.genre_to_index[genre_id], 0)

      feature_vec.append(temp_vec)

    return np.array(feature_vec)

  def _vectorize_single_movie(self, movie):
    movie_genres = movie["genre_ids"].split(",")
    vector = []

    for genre in self.all_genres:
      if genre in list(map(int(movie_genres))):
        vector.append(1)
      else:
        vector.append(0)

    return vector
