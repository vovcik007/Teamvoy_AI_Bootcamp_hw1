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
    date: Optional[date] = None

class DailyLogResponse(DailyLogBase):
    id: int
    date: date

    model_config = ConfigDict(from_attributes=True)