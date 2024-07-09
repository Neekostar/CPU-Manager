from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class CPULoad(Base):
    __tablename__ = 'cpu_load'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    value = Column(Float, nullable=False)

    """
    This class represents the CPU load data.

    Attributes:
        id (Integer): Unique identifier for the CPU load data.
        timestamp (DateTime): The timestamp when the CPU load data was recorded.
        value (Float): The CPU load value at the given timestamp.
    """

    def __init__(self, timestamp: DateTime, value: Float):
        """
        Initialize a new instance of the CPULoad class.

        Args:
            timestamp (DateTime): The timestamp when the CPU load data was recorded.
            value (Float): The CPU load value at the given timestamp.
        """
        self.timestamp = timestamp
        self.value = value


class ServiceStatus(Base):
    __tablename__ = 'service_status'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    is_active = Column(Boolean, nullable=False)

    def update_status(self, is_active: bool):
        """
        Update the status of the service.

        Args:
            is_active (bool): A boolean value indicating whether the service is active or not.

        Returns:
            None: This method does not return any value. It updates the 'is_active' attribute of the ServiceStatus instance.
        """
        self.is_active = is_active
