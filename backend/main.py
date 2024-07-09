from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/cpu_loads_with_gaps")
def get_cpu_loads_with_gaps(db: Session = Depends(get_db)):
    cpu_loads, gaps = crud.get_cpu_loads_with_gaps(db)
    return {
        "cpu_loads": [{"timestamp": load.timestamp, "value": load.value} for load in cpu_loads],
        "gaps": gaps
    }


@app.get("/average_load_last_hour")
def get_average_load_last_hour(db: Session = Depends(get_db)):
    avg_loads = crud.compute_average_load_per_minute(db)
    return avg_loads


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
