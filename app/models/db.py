from sqlalchemy import Column, Float, String, Integer, Boolean
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
    params = Column(String)
    storage_temperature = Column(Float)
    start_pressure = Column(Integer)
    work_pressure = Column(Integer)
    z_value = Column(Float, default='(work_pressure - start_pressure) / (storage_temperature - work_temperature)')
    work_temperature = Column(Float)
    target_pressure = Column(Integer , default='(work_pressure - start_pressure) / (storage_temperature - work_temperature)')