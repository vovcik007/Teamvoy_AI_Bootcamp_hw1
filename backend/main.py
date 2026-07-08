from datetime import date, datetime
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
from datetime import date

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Health Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/logs/", response_model=schemas.DailyLogResponse)
def create_or_update_log(log: schemas.DailyLogCreate, db: Session = Depends(database.get_db)):
    # Default to today
    target_date = date.today()
    
    # If a date string was provided, parse it
    if log.date:
        target_date = datetime.strptime(log.date, "%Y-%m-%d").date()

    db_log = db.query(models.DailyLog).filter(models.DailyLog.date == target_date).first()
    
    if db_log:
        for key, value in log.model_dump(exclude_unset=True, exclude={'date'}).items():
            setattr(db_log, key, value)
    else:
        db_log = models.DailyLog(**log.model_dump(exclude={'date'}))
        db_log.date = target_date
        db.add(db_log)
        
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs/", response_model=list[schemas.DailyLogResponse])
def get_logs(skip: int = 0, limit: int = 30, db: Session = Depends(database.get_db)):
    return db.query(models.DailyLog).order_by(models.DailyLog.date.desc()).offset(skip).limit(limit).all()

@app.get("/stats/", response_model=schemas.HealthStats)
def get_health_stats(db: Session = Depends(database.get_db)):
    logs = db.query(models.DailyLog).all()
    
    if not logs:
        return schemas.HealthStats(
            avg_mood=0.0, avg_sleep=0.0, avg_water=0.0, 
            total_logs=0, insight="Log some data to see your insights!"
        )

    total = len(logs)
    avg_mood = sum(log.mood for log in logs) / total
    avg_sleep = sum(log.sleep_hours for log in logs) / total
    avg_water = sum(log.water_liters for log in logs) / total

    # Robust correlation logic: Compare mood on best sleep days vs worst sleep days
    insight = "Not enough data for sleep correlation."
    
    if total >= 2:
        # Sort logs by sleep hours to split into 'less sleep' and 'more sleep' groups
        sorted_logs = sorted(logs, key=lambda x: x.sleep_hours)
        mid = total // 2
        
        less_sleep_logs = sorted_logs[:mid]
        more_sleep_logs = sorted_logs[mid:]
        
        if less_sleep_logs and more_sleep_logs:
            avg_mood_less_sleep = sum(log.mood for log in less_sleep_logs) / len(less_sleep_logs)
            avg_mood_more_sleep = sum(log.mood for log in more_sleep_logs) / len(more_sleep_logs)
            
            diff = avg_mood_more_sleep - avg_mood_less_sleep
            
            if diff > 0.5:
                insight = f"Your mood is significantly better (avg {avg_mood_more_sleep:.1f}) on days you get more sleep, compared to days you get less (avg {avg_mood_less_sleep:.1f})."
            elif diff < -0.5:
                insight = f"Interestingly, your mood is higher on days you sleep less (avg {avg_mood_less_sleep:.1f}) compared to days you sleep more (avg {avg_mood_more_sleep:.1f})."
            else:
                insight = "Your mood seems relatively consistent regardless of how much you sleep."

    return schemas.HealthStats(
        avg_mood=round(avg_mood, 1),
        avg_sleep=round(avg_sleep, 1),
        avg_water=round(avg_water, 1),
        total_logs=total,
        insight=insight
    )