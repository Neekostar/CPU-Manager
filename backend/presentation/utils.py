import asyncio
import psutil
from sqlalchemy.orm import Session
from infrastructure.repositories.cpu_load_repository import CPULoadRepository


async def save_cpu_load(db: Session) -> None:
    """
    This function continuously saves the CPU load percentage to the database.

    :param db: A SQLAlchemy Session object that represents a database connection.
    :type db: Session

    :return: None
    :rtype: None
    """
    repo = CPULoadRepository(db)
    while True:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        repo.create_cpu_load(cpu_percent)
        await asyncio.sleep(5)
