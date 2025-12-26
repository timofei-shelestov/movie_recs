import asyncio
import json
from src.db import db_connection, movie_ops
from src.data_fetching.tmdb_fetcher import fetch_pages_async


async def collect_movies(pages):
  async with db_connection():
    res = await fetch_pages_async(pages) 
    raw_data = []

    for page in res:
      if page:
        raw_data.extend(page["results"])

    await save_to_json(raw_data, "raw_data.json")

    movies = remove_unnecessary_attributes(raw_data)
    movies = remove_if_empty_date(movies)
    cleaned_movies = remove_duplicates(movies)
    await save_to_db(cleaned_movies)


def remove_unnecessary_attributes(raw_data):
  movies = [
    {
      "id": movie["id"],
      "title": movie["title"],
      "genres": movie["genre_ids"],
      "vote_average": movie["vote_average"],
      "vote_count": movie["vote_count"],
      "release_date": movie["release_date"]
    }
    for movie in raw_data
  ]
  
  return movies


def remove_duplicates(data):
  unique_list = []

  for item in data:
    if item not in unique_list:
      unique_list.append(item)

  return unique_list    


def remove_if_empty_date(movies):
  return [movie for movie in movies if movie.get("release_date")]


async def save_to_json(data, filename):
  with open(f"data/{filename}", "w") as f:
    json.dump(data, f, indent=4)


async def save_to_db(movies):
  return await movie_ops.bulk_create(movies)


if __name__ == "__main__":
    asyncio.run(collect_movies(40))