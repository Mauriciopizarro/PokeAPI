from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.schemas import BerryStats
from app.services import get_all_berry_stats

app = FastAPI(title="Poke-Berries Statistics API")

@app.get("/allBerryStats", response_model=BerryStats)
async def all_berry_stats():
    """
    Endpoint with statistics from all berries.
    """
    try:
        return get_all_berry_stats()
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
            media_type="application/json"
        )
