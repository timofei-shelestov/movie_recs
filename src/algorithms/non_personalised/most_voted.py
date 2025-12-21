import json
from src.data_fetching import data_collector

def get_most_voted(all_movies, amount_of_movies): 
  max_vote_count = max(movie["vote_count"] for movie in all_movies)
  most_voted = []

  while len(most_voted) < amount_of_movies and max_vote_count >= 1000:
    max_vote_indices = [i for i, val in enumerate(all_movies) if val["vote_count"] == max_vote_count]
    if len(max_vote_indices) > 0:
      new_list = (all_movies[i] for i in max_vote_indices)
      most_voted.append(*new_list)
    max_vote_count = max_vote_count - 1

  return list(most_voted)


with open("data/movies.json") as f:
    d = json.load(f)

most_voted = get_most_voted(d, 100)

data_collector.save_data(most_voted, "most_voted")
