from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn
import models
import crud
from database import SessionLocal, engine
from utils import save_cpu_load
import asyncio
import threading

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_save_cpu_load():
    db = SessionLocal()
    asyncio.run(save_cpu_load(db))


@app.on_event("startup")
def startup_event():
    threading.Thread(target=run_save_cpu_load, daemon=True).start()


@app.get("/cpu_load_last_hour")
def get_cpu_load_last_hour(db: Session = Depends(get_db)):
    cpu_loads = crud.get_cpu_loads_last_hour(db)
    return [{"timestamp": load.timestamp, "value": load.value} for load in cpu_loads]


@app.get("/average_load_last_hour")
def get_average_load_last_hour(db: Session = Depends(get_db)):
    avg_load = crud.compute_average_load_per_minute(db)
    return {"average_load_last_hour": avg_load}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
