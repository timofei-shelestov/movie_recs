from src.db import Movie

class MovieOperations:
  async def create(self, movie: dict) -> Movie:
    return Movie.create(movie)

  async def bulk_create(self, movies: list[dict]) -> int:
    Movie.bulk_create(movies)

  async def get_all(self) -> list[Movie]:
      return await Movie.all()

  async def get_by_id(self, movie_id: int) -> Movie | None:
    return await Movie.filter(id=movie_id).first()

  async def get_most_recent(self, limit: int = 10) -> list[Movie]:
    return await Movie.all().order_by("-release_date").limit(limit)

  async def get_top_rated(self, limit: int = 10) -> list[Movie]:
    return await Movie.all().order_by("-vote_average").limit(limit)

  async def get_most_voted(self, limit: int = 10) -> list[Movie]:
    return await Movie.all().order_by("-vote_count").limit(limit)

  async def create(self, data: dict) -> Movie:
    return await Movie.create(**data)

  async def count(self) -> int:
    return await Movie.all().count()

  async def exists(self, movie_id: int) -> bool:
    return await Movie.filter(id=movie_id).exists()

movie_ops = MovieOperations()