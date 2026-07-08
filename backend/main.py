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