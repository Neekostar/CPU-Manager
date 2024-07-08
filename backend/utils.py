import asyncio
from sqlalchemy.orm import Session
import psutil
import crud


async def save_cpu_load(db: Session):
    while True:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        crud.create_cpu_load(db, cpu_percent)
        await asyncio.sleep(5)
