import aiohttp
import asyncio
from config import settings


async def fetch_single_page(session, page_num):
  url = f"{settings.TMDB_BASE_URL}/movie/popular"
  headers = {"Authorization": f"Bearer {settings.TMDB_API_KEY}"}
  params = {"page": page_num, "language": "en-US"}

  async with session.get(url, headers=headers, params=params) as response:
    if response.status == 200:
      if response.content_type == "application/json":
        return await response.json()
      else:
        print(f"Error fetching page {page_num}: provided response is not JSON")
        return None

    else:
      print(f"Error fetching page {page_num}: {response.status}")
      return None


async def fetch_pages_async(pages):
  async with aiohttp.ClientSession() as session:
    tasks = [fetch_single_page(session, page) for page in range(1, pages + 1)]
    results = await asyncio.gather(*tasks)
    if tasks != None:
      return results
    return None
