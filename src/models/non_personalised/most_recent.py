import datetime
import json
from src.data_fetching import data_collector

def get_most_recent(movies):
  curr_date = datetime.datetime.now().date()
  oldest_date = curr_date - datetime.timedelta(weeks=24)
  filtered_movies = [] 

  while curr_date >= oldest_date:
    for movie in movies:
      if movie["release_date"] == "":
        print(movie)
      movie_date = datetime.datetime.strptime(movie["release_date"], "%Y-%m-%d").date()
      if movie_date <= curr_date and movie_date >= oldest_date:
        filtered_movies.append(movie)

    curr_date = curr_date - datetime.timedelta(days=1)
  
  return filtered_movies


with open("data/movies.json") as f:
    d = json.load(f)

most_recent = get_most_recent(d)

data_collector.save_data(most_recent, "most_recent")
