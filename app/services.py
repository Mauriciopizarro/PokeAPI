import httpx
from fastapi_cache.decorator import cache
from collections import Counter

from app.config import settings
from app.utils import calculate_stats, generate_histogram


async def fetch_all_berries():
    response = httpx.get(f"{settings.POKEAPI_BASE_URL}/berry/?limit=1000", timeout=10)
    response.raise_for_status()
    berries_list = response.json()["results"]

    berries_data = []
    growth_times = []

    for berry in berries_list:
        r_berry = httpx.get(berry["url"], timeout=10)
        r_berry.raise_for_status()
        data = r_berry.json()
        berries_data.append(data["name"])
        growth_times.append(data["growth_time"])

    return berries_data, growth_times

@cache(expire=settings.CACHE_EXPIRE)
async def get_all_berry_stats():
    berries, growth_times = await fetch_all_berries()
    freq = {int(k): v for k, v in Counter(growth_times).items()}
    return calculate_stats(berries, growth_times, freq)

@cache(expire=settings.CACHE_EXPIRE)
async def get_berry_histogram():
    berries, growth_times = await fetch_all_berries()
    return generate_histogram(growth_times)
