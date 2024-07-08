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
    ).order_by(models.CPULoad.timestamp).all()

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


def get_service_status_gaps(cpu_loads):
    gaps = []
    threshold = timedelta(seconds=10)
    current_period = None

    for i in range(1, len(cpu_loads)):
        current = cpu_loads[i]
        previous = cpu_loads[i - 1]
        if current.timestamp - previous.timestamp > threshold:
            if current_period:
                current_period['end_time'] = previous.timestamp
                gaps.append(current_period)
            gaps.append({
                "start_time": previous.timestamp,
                "end_time": current.timestamp,
                "is_active": False
            })
            current_period = None
        else:
            if not current_period:
                current_period = {
                    "start_time": previous.timestamp,
                    "is_active": True
                }

    if current_period:
        current_period['end_time'] = cpu_loads[-1].timestamp
        gaps.append(current_period)

    return gaps


def get_cpu_loads_with_gaps(db: Session):
    cpu_loads = get_cpu_loads_last_hour(db)
    gaps = get_service_status_gaps(cpu_loads)
    return cpu_loads, gaps


def update_service_status(db: Session, is_active: bool):
    db_status = models.ServiceStatus(is_active=is_active)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status
