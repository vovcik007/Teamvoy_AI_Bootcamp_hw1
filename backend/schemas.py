from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class DailyLogBase(BaseModel):
    water_liters: float = 0.0
    meals_count: int = 0
    sugar_grams: float = 0.0
    sleep_hours: float = 0.0
    work_hours: float = 0.0
    mood: int = 5

class DailyLogCreate(DailyLogBase):
    date: Optional[str] = None  # Changed to str to accept frontend input easily

class DailyLogResponse(DailyLogBase):
    id: int
    date: date

    model_config = ConfigDict(from_attributes=True)

class HealthStats(BaseModel):
    avg_mood: float
    avg_sleep: float
    avg_water: float
    total_logs: int
    insight: str

    model_config = ConfigDict(from_attributes=True)
