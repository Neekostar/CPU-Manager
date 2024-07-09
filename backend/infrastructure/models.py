from sqlalchemy import Column, Integer, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class CPULoad(Base):
    __tablename__ = 'cpu_load'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    value = Column(Float, nullable=False)

    """
    This class represents a CPU load record in the database.

    Attributes:
        id (Integer): The unique identifier for the CPU load record.
        timestamp (DateTime): The timestamp when the CPU load was recorded.
        value (Float): The CPU load value at the time of recording.

    Methods:
        __repr__(self) -> str:
            Return a string representation of the CPU load record.

        __eq__(self, other: 'CPULoad') -> bool:
            Check if two CPU load records are equal.

        __hash__(self) -> int:
            Return a hash value for the CPU load record.

    """

    def __repr__(self) -> str:
        """
        Return a string representation of the CPU load record.

        Returns:
            str: A string representation of the CPU load record.

        """
        return f"CPULoad(id={self.id}, timestamp={self.timestamp}, value={self.value})"

    def __eq__(self, other: 'CPULoad') -> bool:
        """
        Check if two CPU load records are equal.

        Args:
            other (CPULoad): Another CPU load record to compare with.

        Returns:
            bool: True if the two CPU load records are equal, False otherwise.

        """
        return self.id == other.id and self.timestamp == other.timestamp and self.value == other.value

    def __hash__(self) -> int:
        """
        Return a hash value for the CPU load record.

        Returns:
            int: A hash value for the CPU load record.

        """
        return hash((self.id, self.timestamp, self.value))


# Create the database tables
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
