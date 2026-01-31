import asyncio
import json
from src.db import db_connection, movie_ops, movie_genre_ops, genre_ops
from src.data_fetching.tmdb_fetcher import fetch_pages_async


async def collect_movies(pages):
  async with db_connection():
    if await genre_ops.get_count() <= 0:
      print("ERROR: please fetch genres before fething movies")
      return False

    res = await fetch_pages_async(pages)
    raw_data = []

    for page in res:
      if page:
        raw_data.extend(page["results"])

    save_to_json(raw_data, "raw_data.json")

    movies = remove_unnecessary_attributes(raw_data)
    movies = remove_if_empty_date(movies)
    cleaned_movies = await remove_duplicates(movies)
    movie_genre_pairs = [
      {"movie_id": movie["id"], "genre_id": genre_id}
      for movie in raw_data
      for genre_id in movie["genre_ids"]
    ]

    await save_to_db(cleaned_movies, movie_genre_pairs)


def remove_unnecessary_attributes(raw_data):
  movies = [
    {
      "id": movie["id"],
      "title": movie["title"],
      "vote_average": movie["vote_average"],
      "vote_count": movie["vote_count"],
      "overview": movie["overview"],
      "release_date": movie["release_date"],
    }
    for movie in raw_data
  ]

  return movies


async def remove_duplicates(data):
  unique_list = []
  unique_ids = list(map(lambda x: x.id, await movie_ops.get_all()))

  for item in data:
    if item["id"] not in unique_ids:
      unique_list.append(item)
      unique_ids.append(item["id"])

  return unique_list


def remove_if_empty_date(movies):
  return [movie for movie in movies if movie.get("release_date")]


def save_to_json(data, filename):
  with open(f"data/{filename}", "w") as f:
    json.dump(data, f, indent=2)


async def save_to_db(movies, movies_genre):
  res = await movie_ops.bulk_create(movies)
  await movie_genre_ops.bulk_create(movies_genre)

  return res


if __name__ == "__main__":
  asyncio.run(collect_movies(40))
