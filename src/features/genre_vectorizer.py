class GenreVectorizer:
  def __init__(self, all_genres):
    self.all_genres = all_genres | None

  def genre_vectorize_one(self, movie_genres):
    vector = []

    for genre in self.all_genres:
      if genre in movie_genres:
        vector.append(1)
      else:
        vector.append(0)

    return vector

  def genre_vectorize_many(self, movies_genres):
    feature_vector = []
    for movie_genres in movies_genres:
      feature_vector.append(self.genre_vectorize_one(movie_genres))

    return feature_vector
