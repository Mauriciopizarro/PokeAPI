from pydantic import BaseModel
from typing import List, Dict

class BerryStats(BaseModel):
    berries_names: List[str]
    min_growth_time: int
    max_growth_time: int
    mean_growth_time: float
    median_growth_time: float
    variance_growth_time: float
    frequency_growth_time: Dict[int, int]
