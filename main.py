import asyncio
from src.data_fetching import collect_movies

asyncio.run(collect_movies(40))
