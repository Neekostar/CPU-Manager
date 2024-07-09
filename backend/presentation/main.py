from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from infrastructure.database import SessionLocal
from infrastructure.repositories.cpu_load_repository import CPULoadRepository
import threading
import asyncio
from presentation.utils import save_cpu_load

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
    """
    Retrieves CPU loads with gaps.

    Args:
    db (Session, optional): A database session object. Defaults to Depends(get_db).

    Returns:
    dict: A dictionary containing the CPU loads and gaps. The 'cpu_loads' key contains a list of dictionaries, where each dictionary has a 'timestamp' and a 'value' key. The 'gaps' key contains a list of timestamps where there are gaps in the CPU load data.
    """
    repo = CPULoadRepository(db)
    cpu_loads, gaps = repo.get_cpu_loads_with_gaps()
    return {
        "cpu_loads": [{"timestamp": load.timestamp, "value": load.value} for load in cpu_loads],
        "gaps": gaps
    }


@app.get("/average_load_last_hour")
def get_average_load_last_hour(db: Session = Depends(get_db)):
    """
    Computes the average CPU load per minute for the last hour.

    Args:
    db (Session, optional): A database session object. Defaults to Depends(get_db).

    Returns:
    dict: A dictionary containing the average CPU load per minute for the last hour. The dictionary has a single key 'avg_loads', which is a list of dictionaries, where each dictionary has a 'minute' and an 'average_load' key. The 'minute' key contains the minute of the hour, and the 'average_load' key contains the average CPU load for that minute.
    """
    repo = CPULoadRepository(db)
    avg_loads = repo.compute_average_load_per_minute()
    return avg_loads


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
