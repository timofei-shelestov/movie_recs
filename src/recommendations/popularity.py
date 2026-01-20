from src.db import operations
import asyncio
from recommendations import BaseRecommender


class PopularityRecommender(BaseRecommender):
  pass


def popularity(movie: dict, n=10):
  return (movie.vote_count / (movie.vote_count + 10) * movie.vote_average) + (
    10 / (movie.vote_count + 10) / 6.8
  )


if __name__ == "__main__":
  movies = asyncio.run(operations.movie_ops.get_by_id())
