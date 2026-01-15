from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from fastapi.responses import HTMLResponse, JSONResponse

from app.config import settings
from app.schemas import BerryStats
from app.services import get_all_berry_stats, get_berry_histogram

app = FastAPI(title="Poke-Berries Statistics API")

@app.on_event("startup")
async def startup():
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="poke-berries")

@app.get("/allBerryStats", response_model=BerryStats)
async def all_berry_stats_endpoint():
    try:
        return await get_all_berry_stats()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/allBerryHistogram", response_class=HTMLResponse)
async def all_berry_histogram_endpoint():
    try:
        return await get_berry_histogram()
    except Exception as e:
        return HTMLResponse(content=f"<p>Error: {e}</p>", status_code=500)
