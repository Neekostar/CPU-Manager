from datetime import datetime, timedelta
from typing import List, Dict
from core.entities.cpu_load import CPULoad


def compute_average_load_per_minute(cpu_loads: List[CPULoad]) -> List[Dict[str, str]]:
    """
    This function computes the average CPU load per minute from a list of CPU load instances.

    Args: cpu_loads (List[CPULoad]): A list of CPU load instances, each containing a timestamp and a value
    representing the CPU load at that timestamp.

    Returns: List[Dict[str, str]]: A list of dictionaries, where each dictionary contains the timestamp and the
    average CPU load for a specific minute.
    """
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
