from src.db import Movie, Genre, MovieGenre


class MovieOperations:
  async def create(self, movie):
    return await Movie.create(**movie)

  async def bulk_create(self, movies):
    return await Movie.bulk_create([Movie(**m) for m in movies])

  async def get_all(self):
    return await Movie.all()

  async def get_by_id(self, movie_id):
    return await Movie.filter(id=movie_id).first()

  async def get_most_recent(self, limit=10):
    return await Movie.all().order_by("-release_date").limit(limit)

  async def get_top_rated(self, limit=10):
    return await Movie.all().order_by("-vote_average").limit(limit)

  async def get_most_voted(self, limit=10):
    return await Movie.all().order_by("-vote_count").limit(limit)

  async def count(self):
    return await Movie.all().count()

  async def exists(self, movie_id):
    return await Movie.filter(id=movie_id).exists()


movie_ops = MovieOperations()


class GenreOperations:
  async def create(self, genre):
    return await Genre.create(**genre)

  async def bulk_create(self, genres):
    return await Genre.bulk_create([Genre(**g) for g in genres])


genre_ops = GenreOperations()


class MovieGenreOperations:
  async def bulk_create(movies_genres):
    return await MovieGenre.bulk_create([MovieGenre(**mg) for mg in movies_genres])


movie_genre_ops = MovieGenreOperations
