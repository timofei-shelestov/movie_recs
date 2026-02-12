from recommendations import BaseRecommender


class PopularityRecommender(BaseRecommender):
  ## weighted rating using Bayesian estimation. Source: https://fulmicoton.com/posts/bayesian_rating/

  def __init__(self, movies):
    super().__init__(movies)

  def score_movie(self, movie):
    C = 5
    m = movie["vote_average"]
    vote_sum = movie["vote_count"] * movie["vote_average"]

    return (C * m + vote_sum) / (C + movie["vote_count"])

  def get_recommendation(self, movies):
    scored = [(movie["id"], self.score_movie(movie)) for movie in self.movies | movies]

    return scored
