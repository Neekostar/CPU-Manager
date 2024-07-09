from typing import List, Dict, Tuple, Union

from sqlalchemy.orm import Session
import models
from datetime import datetime, timedelta


def create_cpu_load(db: Session, value: float) -> models.CPULoad:
    """
    Creates a new CPU load entry in the database with the specified value.

    :param db: A SQLAlchemy Session object representing the database connection.
    :param value: The value of the CPU load to be created.
    :return: The newly created :class:`models.CPULoad` object.
    """
    db_load = models.CPULoad(value=value)
    db.add(db_load)
    db.commit()
    db.refresh(db_load)
    return db_load


def get_cpu_loads_last_hour(db: Session) -> List[models.CPULoad]:
    """
    Retrieves CPU loads from the database for the last hour.

    :param db: A SQLAlchemy Session object representing the database connection.
    :return: A list of :class:`models.CPULoad` objects representing the CPU loads for the last hour.
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)

    cpu_loads = db.query(models.CPULoad).filter(
        models.CPULoad.timestamp >= start_time,
        models.CPULoad.timestamp <= end_time
    ).order_by(models.CPULoad.timestamp).all()

    return cpu_loads


def compute_average_load_per_minute(db: Session) -> List[Dict[str, str]]:
    """
    Computes the average CPU load per minute for the last hour and returns a list of dictionaries containing the timestamp and average load for each minute.

    :param db: A SQLAlchemy Session object representing the database connection.
    :return: A list of dictionaries where each dictionary contains the timestamp and average CPU load for a minute in the last hour.
    """
    cpu_loads = get_cpu_loads_last_hour(db)

    average_load_per_minute = {}

    for load in cpu_loads:
        minute_start = load.timestamp.replace(second=0, microsecond=0)

        if minute_start in average_load_per_minute:
            continue

        loads_in_minute = [load.value for load in cpu_loads
                           if minute_start <= load.timestamp < minute_start + timedelta(minutes=1)]

        if loads_in_minute:
            average_load = sum(loads_in_minute) / len(loads_in_minute)
        else:
            average_load = 0.0

        average_load_per_minute[minute_start] = {
            "timestamp": minute_start.strftime('%Y-%m-%d %H:%M'),
            "average_load": average_load
        }

    formatted_avg_loads = list(average_load_per_minute.values())

    return formatted_avg_loads


def get_service_status_gaps(cpu_loads):
    """
    This function identifies gaps in the CPU load data where the CPU load has been inactive for more than a specified threshold (default 10 seconds).

    :param cpu_loads: A list of :class:`models.CPULoad` objects representing the CPU loads for the last hour.
    :type cpu_loads: List[models.CPULoad]
    :return: A list of dictionaries where each dictionary contains the start and end times of a gap in CPU load activity, along with a boolean indicating whether the CPU was active during that period.
    :rtype: List[Dict[str, Union[datetime, bool]]]
    """
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


def get_cpu_loads_with_gaps(db: Session) -> Tuple[List[models.CPULoad], List[Dict[str, Union[datetime, bool]]]]:
    """
    Retrieves CPU loads from the database for the last hour along with the gaps in CPU load activity.

    :param db: A SQLAlchemy Session object representing the database connection.
    :return: A tuple containing a list of :class:`models.CPULoad` objects representing the CPU loads for the last hour and a list of dictionaries where each dictionary contains the start and end times of a gap in CPU load activity, along with a boolean indicating whether the CPU was active during that period.
    """
    cpu_loads = get_cpu_loads_last_hour(db)
    gaps = get_service_status_gaps(cpu_loads)
    return cpu_loads, gaps


def update_service_status(db: Session, is_active: bool) -> models.ServiceStatus:
    """
    Updates the service status in the database.

    :param db: A SQLAlchemy Session object representing the database connection.
    :type db: Session
    :param is_active: A boolean value indicating whether the service is active or not.
    :type is_active: bool
    :return: The newly created :class:`models.ServiceStatus` object.
    :rtype: models.ServiceStatus
    """
    db_status = models.ServiceStatus(is_active=is_active)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status
