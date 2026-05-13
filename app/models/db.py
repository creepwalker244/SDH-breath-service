from sqlalchemy import Column, Float, String, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    group = Column(String)

    def __repr__(self):
        
        return f"User(username={self.username}, email={self.email}, group={self.group})"
    

class CalculationParams(Base):
    __tablename__ = "calculation_params"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
#    params = Column(String)
    storage_temperature = Column(Float)
    base_pressure = Column(Integer)
    z_value_base = Column(Float)
    work_pressure = Column(Integer)
    work_time_start = Column(DateTime)
    end_pressure = Column(Integer)
    work_time_end = Column(DateTime)
    total_time = Column(Integer, default='work_time_end - work_time_start')
    z_value_work = Column(Float)
    work_temperature = Column(Float)
    target_pressure = Column(Float)
    target_temperature = Column(Float)
    true_volume = Column(Float)
    baloon_volume = Column(Float)