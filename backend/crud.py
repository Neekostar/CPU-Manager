from sqlalchemy.orm import Session
import models
from datetime import datetime, timedelta
from sqlalchemy import func


def create_cpu_load(db: Session, value: float):
    db_load = models.CPULoad(value=value)
    db.add(db_load)
    db.commit()
    db.refresh(db_load)
    return db_load


def get_cpu_loads_last_hour(db: Session):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)

    cpu_loads = db.query(models.CPULoad).filter(
        models.CPULoad.timestamp >= start_time,
        models.CPULoad.timestamp <= end_time
    ).all()

    return cpu_loads


def compute_average_load_per_minute(db: Session):
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)

    avg_loads = db.query(func.avg(models.CPULoad.value).label('average_load'), models.CPULoad.timestamp).filter(
        models.CPULoad.timestamp >= start_time,
        models.CPULoad.timestamp <= end_time
    ).group_by(
        func.strftime('%Y-%m-%d %H:%M', models.CPULoad.timestamp)
    ).all()

    formatted_avg_loads = [{"timestamp": load.timestamp, "average_load": load.average_load} for load in avg_loads]

    return formatted_avg_loads
