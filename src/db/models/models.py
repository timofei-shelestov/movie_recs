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


async def run():
  await Tortoise.init(db_url="sqlite://movies_db.sqlite3", modules={"models": ["__main__"]})
  await Tortoise.generate_schemas() 


def patch_aiosqlite_for_tortoise():
    import aiosqlite
    if hasattr(aiosqlite.Connection, "start"):
        return
    def start(self):
        if not self._thread.is_alive():
            self._thread.start()
    aiosqlite.Connection.start = start


if __name__ == "__main__": 
  patch_aiosqlite_for_tortoise()
  run_async(run())

  print(run_async(Movie.all()))
