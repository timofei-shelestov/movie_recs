from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise import fields 

class Movie(Model):
  title = fields.CharField(max_length=255, db_index=True)
  genres: fields.ManyToManyRelation["Genre"] = fields.ManyToManyField(
      "models.Genre", related_name="movies", through="movie_genre"
    )
  vote_average = fields.FloatField()
  vote_count = fields.IntField()
  release_date = fields.DatetimeField()


class Genre(Model):
  title = fields.CharField(max_length=255, db_index=True)
  movies: fields.ManyToManyRelation[Movie]

