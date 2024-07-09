from sqlalchemy.orm import Session
from infrastructure.models import CPULoad
from typing import List, Dict, Tuple
from datetime import datetime, timedelta


class CPULoadRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_cpu_load(self, value: float) -> CPULoad:
        db_load = CPULoad(value=value)
        self.db.add(db_load)
        self.db.commit()
        self.db.refresh(db_load)
        return db_load

    def get_cpu_loads_last_hour(self) -> List[CPULoad]:
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        return self.db.query(CPULoad).filter(CPULoad.timestamp >= start_time, CPULoad.timestamp <= end_time).order_by(CPULoad.timestamp).all()

    def get_service_status_gaps(self, cpu_loads: List[CPULoad]) -> List[Dict[str, datetime]]:
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

    def get_cpu_loads_with_gaps(self) -> Tuple[List[CPULoad], List[Dict[str, datetime]]]:
        cpu_loads = self.get_cpu_loads_last_hour()
        gaps = self.get_service_status_gaps(cpu_loads)
        return cpu_loads, gaps

    def compute_average_load_per_minute(self) -> List[Dict[str, str]]:
        cpu_loads = self.get_cpu_loads_last_hour()
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

        return list(average_load_per_minute.values())
