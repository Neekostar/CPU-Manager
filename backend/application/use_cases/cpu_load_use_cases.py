from typing import List, Dict
from core.services.cpu_load_service import compute_average_load_per_minute
from infrastructure.repositories.cpu_load_repository import CPULoadRepository
from sqlalchemy.orm import Session


def get_average_load_last_hour(db: Session) -> List[Dict[str, str]]:
    """
    Calculates the average CPU load per minute for the last hour.

    Args:
    db (Session): A SQLAlchemy session object representing the database connection.

    Returns: List[Dict[str, str]]: A list of dictionaries containing the average CPU load per minute for the last
    hour. Each dictionary contains a 'minute' key with the corresponding minute value and a 'load' key with the
    average CPU load for that minute.
    """
    repo = CPULoadRepository(db)
    cpu_loads = repo.get_cpu_loads_last_hour()
    return compute_average_load_per_minute(cpu_loads)
