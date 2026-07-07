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
    target_date = log.date or date.today()
    db_log = db.query(models.DailyLog).filter(models.DailyLog.date == target_date).first()
    
    if db_log:
        # Use model_dump for Pydantic V2
        for key, value in log.model_dump(exclude_unset=True).items():
            setattr(db_log, key, value)
    else:
        db_log = models.DailyLog(**log.model_dump())
        db.add(db_log)
        
    db.commit()
    db.refresh(db_log)
    return db_log

@app.get("/logs/", response_model=list[schemas.DailyLogResponse])
def get_logs(skip: int = 0, limit: int = 30, db: Session = Depends(database.get_db)):
    return db.query(models.DailyLog).order_by(models.DailyLog.date.desc()).offset(skip).limit(limit).all()