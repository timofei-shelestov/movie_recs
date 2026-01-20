from abc import ABC, abstractmethod


class BaseRecommender(ABC):
  def __init__(self, movies=None):
    self.movies = movies or None

  def load_movies(self, movies):
    self.movies = movies

  @abstractmethod
  def get_recommendations():
    pass
