import pytest
import json
from unittest.mock import patch, mock_open, AsyncMock
from src.data_fetching.data_collector import (
  collect_movies,
  remove_unnecessary_attributes,
  remove_duplicates,
  save_data,
)


@pytest.mark.asyncio
async def test_collect_movies():
  mock_pages_response = [
    {
      "results": [
        {
          "id": 1,
          "title": "Movie 1",
          "genre_ids": [1, 2],
          "vote_average": 8.5,
          "vote_count": 1000,
          "overview": "This is movie 1",
          "poster_path": "/path1.jpg",
        },
        {
          "id": 2,
          "title": "Movie 2",
          "genre_ids": [3, 4],
          "vote_average": 7.2,
          "vote_count": 500,
          "overview": "This is movie 2",
          "poster_path": "/path2.jpg",
        },
      ]
    },
    {
      "results": [
        {
          "id": 1,
          "title": "Movie 1",
          "genre_ids": [1, 2],
          "vote_average": 8.5,
          "vote_count": 1000,
          "overview": "This is movie 1",
          "poster_path": "/path1.jpg",
        }
      ]
    },
  ]

  with patch(
    "src.data_fetching.data_collector.fetch_pages_async", new_callable=AsyncMock
  ) as mock_fetch:
    with patch("src.data_fetching.data_collector.save_data") as mock_save:
      mock_fetch.return_value = mock_pages_response

      await collect_movies([1, 2])

      mock_fetch.assert_called_once_with([1, 2])
      assert mock_save.call_count == 2

      raw_data_call = mock_save.call_args_list[0]
      movies_call = mock_save.call_args_list[1]

      assert len(raw_data_call[0][0]) == 3
      assert raw_data_call[0][1] == "raw_data"

      assert len(movies_call[0][0]) == 2
      assert movies_call[0][1] == "movies"

      expected_movie = {
        "id": 1,
        "title": "Movie 1",
        "genre_ids": [1, 2],
        "vote_average": 8.5,
        "vote_count": 1000,
      }
      assert expected_movie in movies_call[0][0]


def test_remove_unnecessary_attributes():
  raw_data = [
    {
      "id": 1,
      "title": "Movie 1",
      "genre_ids": [1, 2],
      "vote_average": 8.5,
      "vote_count": 1000,
      "overview": "This is movie 1",
      "poster_path": "/path1.jpg",
      "release_date": "2023-01-01",
    },
    {
      "id": 2,
      "title": "Movie 2",
      "genre_ids": [3, 4],
      "vote_average": 7.2,
      "vote_count": 500,
      "overview": "This is movie 2",
      "poster_path": "/path2.jpg",
      "release_date": "2023-02-01",
    },
  ]

  result = remove_unnecessary_attributes(raw_data)

  expected = [
    {
      "id": 1,
      "title": "Movie 1",
      "genre_ids": [1, 2],
      "vote_average": 8.5,
      "vote_count": 1000,
    },
    {
      "id": 2,
      "title": "Movie 2",
      "genre_ids": [3, 4],
      "vote_average": 7.2,
      "vote_count": 500,
    },
  ]

  assert result == expected


def test_remove_duplicates():
  data = [
    {"id": 1, "title": "Movie 1"},
    {"id": 2, "title": "Movie 2"},
    {"id": 1, "title": "Movie 1"},
    {"id": 3, "title": "Movie 3"},
    {"id": 2, "title": "Movie 2"},
  ]

  result = remove_duplicates(data)

  assert len(result) == 3
  assert {"id": 1, "title": "Movie 1"} in result
  assert {"id": 2, "title": "Movie 2"} in result
  assert {"id": 3, "title": "Movie 3"} in result


def test_remove_duplicates_empty_list():
  result = remove_duplicates([])
  assert result == []


def test_save_data():
  test_data = [{"id": 1, "title": "Movie 1"}, {"id": 2, "title": "Movie 2"}]

  mock_file = mock_open()

  with patch("builtins.open", mock_file):
    save_data(test_data, "test_movies")

    mock_file.assert_called_once_with("data/test_movies.json", "w")
    handle = mock_file()

    written_content = "".join(call.args[0] for call in handle.write.call_args_list)
    parsed_content = json.loads(written_content)

    assert parsed_content == test_data


def test_save_data_creates_proper_filename():
  test_data = {"key": "value"}

  mock_file = mock_open()

  with patch("builtins.open", mock_file):
    save_data(test_data, "custom_name")

    mock_file.assert_called_once_with("data/custom_name.json", "w")
