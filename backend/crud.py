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

    avg_loads = db.query(
        func.strftime('%Y-%m-%d %H:%M', models.CPULoad.timestamp).label('minute'),
        func.avg(models.CPULoad.value).label('average_load')
    ).filter(
        models.CPULoad.timestamp >= start_time,
        models.CPULoad.timestamp <= end_time
    ).group_by('minute').all()

    formatted_avg_loads = [{"timestamp": minute, "average_load": average_load} for minute, average_load in avg_loads]

    return formatted_avg_loads
