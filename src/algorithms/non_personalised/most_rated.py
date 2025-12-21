import json
from src.data_fetching import data_collector
from src.utils import plot

def get_most_voted(all_movies, amount_of_movies): 
  max_vote_average = max(movie["vote_average"] for movie in all_movies)
  most_rated = []

  while len(most_rated) < amount_of_movies and max_vote_average >= 8.0:
    max_vote_indices = [i for i, val in enumerate(all_movies) if val["vote_average"] == max_vote_average]
    if len(max_vote_indices) > 0:
      new_list = (all_movies[i] for i in max_vote_indices)
      most_rated.append(list(new_list))
    max_vote_average = max_vote_average - 1

  return list(most_rated)


with open("data/movies.json") as f:
    d = json.load(f)

most_rated = get_most_voted(d, 100)

data_collector.save_data(most_rated, "most_rated")

plot.bar(list(map(lambda movie : int(movie["vote_average"])), list(most_rated)), 10, list(map(lambda movie : movie["title"], list(most_rated))), "Most Rated")
