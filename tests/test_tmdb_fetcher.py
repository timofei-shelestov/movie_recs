import pytest
from aioresponses import aioresponses
import aiohttp
from config import settings
from src.data_fetching import tmdb_fetcher

SUCCESS_STATUS = 200
BAD_STATUS = 500

valid_content_type_header = {"Content-Type": "application/json"}

invalid_content_type_header = {"Content-Type": "application/javascript"}


json_response = {
  "page": 1,
  "results": [
    {"id": 123, "title": "Test Movie", "vote_average": 8.5},
    {"id": 456, "title": "Another Movie", "vote_average": 7.2},
  ],
  "total_pages": 500,
  "total_results": 10000,
}


@pytest.mark.asyncio
async def test_successful_response():
  session = aiohttp.ClientSession()

  with aioresponses() as mocked:
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=1&language=en-US",
      status=SUCCESS_STATUS,
      payload=json_response,
      headers=valid_content_type_header,
    )
    res = await tmdb_fetcher.fetch_single_page(session, 1)

    await session.close()

    mocked.assert_called_once()
    assert res is not None
    assert res["page"] == 1
    assert len(res["results"]) == 2
    assert res["results"][0]["title"] == "Test Movie"


@pytest.mark.asyncio
async def test_error_code_response():
  session = aiohttp.ClientSession()

  with aioresponses() as mocked:
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=1&language=en-US",
      status=BAD_STATUS,
      payload=json_response,
      headers=valid_content_type_header,
    )
    res = await tmdb_fetcher.fetch_single_page(session, 1)

    await session.close()

  mocked.assert_called_once()
  assert res is None


@pytest.mark.asyncio
async def test_invalid_content_type_response():
  session = aiohttp.ClientSession()

  with aioresponses() as mocked:
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=1&language=en-US",
      payload=json_response,
      headers=invalid_content_type_header,
    )
    res = await tmdb_fetcher.fetch_single_page(session, 1)

    await session.close()

  mocked.assert_called_once()
  assert res is None


@pytest.mark.asyncio
async def test_multiple_page_response():
  with aioresponses() as mocked:
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=1&language=en-US",
      payload=json_response,
      headers=valid_content_type_header,
      repeat=True,
    )
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=2&language=en-US",
      payload=json_response,
      headers=valid_content_type_header,
      repeat=True,
    )
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=3&language=en-US",
      payload=json_response,
      headers=valid_content_type_header,
      repeat=True,
    )
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=4&language=en-US",
      payload=json_response,
      headers=valid_content_type_header,
      repeat=True,
    )
    mocked.get(
      f"{settings.TMDB_BASE_URL}/movie/popular?page=5&language=en-US",
      payload=json_response,
      headers=valid_content_type_header,
      repeat=True,
    )

    res = await tmdb_fetcher.fetch_pages_async(5)
  assert res is not None
