import asyncio
from sqlalchemy.orm import Session
import psutil
import crud


async def save_cpu_load(db: Session) -> None:
    """
    This function continuously saves the CPU load percentage to the database.

    :param db: A SQLAlchemy Session object that represents a database connection.
    :type db: Session

    The function uses the `psutil` library to get the CPU load percentage every 1 second (interval=1) and
    averages it across all CPUs (percpu=False). It then creates a new `cpu_load` record in the database
    using the `crud.create_cpu_load` function. The function then sleeps for 5 seconds before repeating the process.

    :return: None
    :rtype: None
    """
    while True:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        crud.create_cpu_load(db, cpu_percent)
        await asyncio.sleep(5)
