import os
import httpx
from app.utils import calculate_stats
from functools import lru_cache


POKEAPI_BASE_URL = os.getenv("POKEAPI_BASE_URL", "https://pokeapi.co/api/v2")


@lru_cache(maxsize=1)
def get_all_berry_stats():
    """
    Get all berries from pokeapi and returns growth_time statistics .
    """
    response = httpx.get(f"{POKEAPI_BASE_URL}/berry/?limit=1000")
    response.raise_for_status()
    berries_list = response.json()["results"]

    berries_data = []
    growth_times = []

    for berry in berries_list:
        r = httpx.get(berry["url"], timeout=10)
        r.raise_for_status()
        data = r.json()
        berries_data.append(data["name"])
        growth_times.append(data["growth_time"])

    stats = calculate_stats(berries_data, growth_times)
    return stats
