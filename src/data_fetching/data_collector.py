import asyncio

import json
from tortoise import Tortoise
from src.data_fetching.tmdb_fetcher import fetch_pages_async
from src.db.models import Movie
from src.db.models.models import patch_aiosqlite_for_tortoise

async def collect_movies(pages):
  res = await fetch_pages_async(pages) 
  raw_data = []

  for page in res:
    raw_data.extend(page["results"])

  ##  await save_data(raw_data, "raw_data")

  movies = remove_unnecessary_attributes(raw_data)
  movies = remove_if_empty_date(movies)
  cleaned_movies = remove_duplicates(movies)
  await save_data(cleaned_movies, "movies")


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
  for movie in movies:
    if movie["release_date"] == "":
      movies.remove(movie)
  return movies

async def save_data(data, filename):
  print("HERE 1")
  patch_aiosqlite_for_tortoise()
  await Tortoise.init(
       db_url="sqlite://movies_db.sqlite3",
       modules={"models": ["src.db.models.models"]}
  )

  print("HERE 2")

  movie_objects = [
    Movie(
      title=movie["title"],
      vote_average=movie["vote_average"],
      vote_count=movie["vote_count"],
      release_date=movie["release_date"]
    )
      for movie in data
  ]
    
  await Movie.bulk_create(movie_objects)

  print("Here 3")


  await Tortoise.close_connections() 

asyncio.run(collect_movies(40))