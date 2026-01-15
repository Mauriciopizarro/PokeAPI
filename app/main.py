from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.services import get_all_berry_stats

app = FastAPI(title="Poke-Berries Statistics API")

@app.get("/allBerryStats", response_class=JSONResponse)
async def all_berry_stats():
    """
    Endpoint with statistics from all berries.
    """
    try:
        stats = get_all_berry_stats()
        return JSONResponse(content=stats, media_type="application/json")
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500,
            media_type="application/json"
        )
