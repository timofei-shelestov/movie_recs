import asyncio

from src.data_fetching import collect_movies


def main() -> None:
    asyncio.run(collect_movies(40))


if __name__ == "__main__":
    main()
