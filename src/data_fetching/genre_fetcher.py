import asyncio
import aiohttp
from config import settings
from src.db import db_connection, genre_ops


async def fetch_genres_async():
  url = f"{settings.TMDB_BASE_URL}/genre/movie/list"
  headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
  params = {"language": "en-US"}
  async with aiohttp.ClientSession() as session:
    async with session.get(url, headers=headers, params=params) as response:
      if response.status == 200:
        if response.content_type == "application/json":
          return await response.json()
        else:
          print("Error fetching genres: provided response is not JSON")
          return None
      else:
        print(f"Error fetching genres: {response.status}")
        return None


async def load_genres_to_db():
  async with db_connection():
    genres = await fetch_genres_async()
    if genres is None:
      print("Error while loading genres to the database")
      return None

    return await genre_ops.bulk_create(genres["genres"])


if __name__ == "__main__":
  asyncio.run(load_genres_to_db())
