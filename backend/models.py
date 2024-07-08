from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class CPULoad(Base):
    __tablename__ = 'cpu_load'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    value = Column(Float, nullable=False)


class ServiceStatus(Base):
    __tablename__ = 'service_status'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
    is_active = Column(Boolean, nullable=False)
