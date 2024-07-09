from datetime import datetime


class CPULoad:
    """
    Represents the CPU load at a given timestamp.

    Attributes:
        value (float): The CPU load value.
        timestamp (datetime): The timestamp when the CPU load was recorded.

    Methods:
        __init__(self, value: float, timestamp: datetime = None): Initializes a new instance of the CPULoad class.
    """

    def __init__(self, value: float, timestamp: datetime = None):
        """
        Initializes a new instance of the CPULoad class.

        Args: value (float): The CPU load value. timestamp (datetime, optional): The timestamp when the CPU load was
        recorded. Defaults to the current time if not provided.
        """
        self.value = value
        self.timestamp = timestamp or datetime.now()
