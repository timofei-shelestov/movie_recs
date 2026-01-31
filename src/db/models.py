from tortoise import fields
from tortoise.models import Model


class Movie(Model):
  title = fields.CharField(max_length=255, db_index=True)
  vote_average = fields.FloatField()
  vote_count = fields.IntField()
  overview = fields.CharField(max_length=1000)
  release_date = fields.DatetimeField()

  class Meta:
    table = "movies"


class Genre(Model):
  name = fields.CharField(max_length=255, db_index=True)

  class Meta:
    table = "genres"


class MovieGenre(Model):
  movie_id = fields.IntField(db_index=True)
  genre_id = fields.IntField(db_index=True)

  class Meta:
    table = "movie_genre"
    indexes = ("movie_id", "genre_id")


class User(Model):
  name = fields.CharField(max_length=100)
  age = fields.IntField(null=True)
  created_at = fields.DatetimeField(auto_now_add=True)

  class Meta:
    table = "users"


class UserRating(Model):
  user = fields.ForeignKeyField("models.User", related_name="ratings")
  movie = fields.ForeignKeyField("models.Movie", related_name="ratings")
  rating = fields.FloatField()
  timestamp = fields.DatetimeField(auto_now_add=True)

  class Meta:
    table = "user_ratings"
    unique_together = (("user", "movie"),)
