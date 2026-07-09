# app/models/models.py
from datetime import datetime
from typing import Optional, List, Required
from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum


# ============ Enums ============
class UserGroup(str, Enum):
    """Группы пользователей"""
    ADMIN = "admin"
    USER = "user"
    ANALYST = "analyst"


# ============ User Schemas ============
class UserBase(BaseModel):
    """Базовая модель пользователя"""
    username: str = Field(..., min_length=3, max_length=50, examples=["ivanov_i"])
    is_active: bool = Field(default=True)
    group: UserGroup = Field(default=UserGroup.USER)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Username cannot be empty')
        return v.strip()


class UserCreate(UserBase):
    """Модель для создания пользователя (email и пароль только здесь)"""
    email: str = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=8, max_length=100, examples=["StrongPass1"])
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v


class UserUpdate(BaseModel):
    """Модель для обновления пользователя"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = None
    is_active: Optional[bool] = None
    group: Optional[UserGroup] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower() if v else v


class UserResponse(BaseModel):
    """Модель для ответа API - только безопасные поля"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    is_active: bool
    group: UserGroup


class UserInDB(BaseModel):
    """Полная модель пользователя из БД (для внутренней работы)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool
    group: UserGroup


# ============ Calculation Schemas ============
class CalculationParamsBase(BaseModel):
    """Базовая модель параметров расчета"""
    storage_temperature: float = Field(..., gt=-273.15, examples=[20.5])
    base_pressure: int = Field(..., gt=0, examples=[100])
    work_pressure: int = Field(..., gt=0, examples=[150])
    work_temperature: float = Field(..., gt=-273.15, examples=[80.0])
    
    #@field_validator('storage_temperature', 'work_temperature')
    #@classmethod
    #def validate_temperature(cls, v: float) -> float:
    #    if v < -273.15:  # Абсолютный ноль
    #        raise ValueError('Temperature cannot be below absolute zero (-273.15°C)')
    #    return v
    
    #@field_validator('start_pressure', 'work_pressure')
    #@classmethod
    #def validate_pressure(cls, v: int) -> int:
    #    if v <= 0:
    #        raise ValueError('Pressure must be positive')
    #    return v


class CalculationParamsCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    storage_temperature: float | None = Field(None, gt=-273.15)
    base_pressure: int | None = Field(None, gt=259, lt=400)
    work_pressure: int = Field(..., gt=0, lt=400) 
    work_time_start: datetime | None = None
    end_pressure: int = Field(..., gt=0, lt=400)
    work_time_end: datetime | None = None
    total_time: int | None = None
    baloon_volume: float = Field(..., gt=0.0)


class CalculationParamsUpdate(BaseModel):
    """Модель для обновления параметров расчета"""
    storage_temperature: Optional[float] = Field(None, gt=-273.15)
    start_pressure: Optional[int] = Field(None, gt=0)
    work_pressure: Optional[int] = Field(None, gt=0)
    work_temperature: Optional[float] = Field(None, gt=-273.15)


class CalculationParamsResponse(BaseModel):
    """Модель для списка расчетов - БЕЗ вычисляемых полей"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    storage_temperature: float
    start_pressure: int
    work_pressure: int
    work_temperature: float


class CalculationResultsResponse(BaseModel):
    """
    Модель с результатами расчетов (только для GET запроса результатов)
    Вычисляемые поля: z_value, target_pressure
    Рассчитываются триггерами БД или бэкендом
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    z_value: Optional[float] = Field(None, description="(work_pressure - start_pressure) / (storage_temperature - work_temperature)")
    target_pressure: Optional[float] = Field(None, description="(work_pressure - start_pressure) / (storage_temperature - work_temperature)")
    calculated_at: Optional[datetime] = Field(None, description="Время последнего расчета")
    
    # Для связи с исходными параметрами
    calculation_params: Optional[CalculationParamsResponse] = None


class CalculationParamsInDB(CalculationParamsResponse):
    """Полная модель из БД с вычисляемыми полями"""
    z_value: Optional[float] = None
    target_pressure: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ============ Response Wrappers ============
class PaginatedResponse(BaseModel):
    """Обертка для пагинированных ответов"""
    items: List
    total: int
    page: int
    size: int
    pages: int


class MessageResponse(BaseModel):
    """Стандартный ответ с сообщением"""
    message: str
    detail: Optional[str] = None


# ============ Связанные модели ============
class UserWithCalculations(UserResponse):
    """Пользователь со списком его расчетов"""
    calculations: Optional[List[CalculationParamsResponse]] = None


class CalculationWithUser(CalculationParamsResponse):
    """Расчет с информацией о пользователе"""
    user: Optional[UserResponse] = None