from sqlalchemy import Column, Integer, Float, Date
from database import Base
import datetime

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.date.today, unique=True, index=True)
    water_liters = Column(Float, default=0.0)
    meals_count = Column(Integer, default=0)
    sugar_grams = Column(Float, default=0.0)
    sleep_hours = Column(Float, default=0.0)
    work_hours = Column(Float, default=0.0)
    mood = Column(Integer, default=5) # 1 to 10