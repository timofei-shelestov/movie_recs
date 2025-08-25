import asyncio

import json
from src.data_fetching.tmdb_fetcher import fetch_pages_async

async def collect_movies(pages):
  res = await fetch_pages_async(pages) 
  raw_data = []

  for page in res:
    raw_data.extend(page["results"])

  save_data(raw_data, "raw_data")

  movies = remove_unnecessary_attributes(raw_data)
  cleaned_movies = remove_duplicates(movies)
  save_data(cleaned_movies, "movies")


def remove_unnecessary_attributes(raw_data):
  movies = [
    {
        "id": movie["id"],
        "title": movie["title"],
        "genre_ids": movie["genre_ids"],
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


def save_data(data, filename):
  with open(f"data/{filename}.json", "w") as f:
    json.dump(data, f, indent=2)
    

asyncio.run(collect_movies(40))