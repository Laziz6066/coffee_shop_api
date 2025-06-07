# app/schemas/user.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# Общие атрибуты, которые не меняются/только для чтения
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False
    is_admin: bool = False

# Схема регистрации (входные данные: email и пароль)
class UserCreate(BaseModel):
    email: EmailStr
    password: str  # простой текстовый пароль, будет захеширован

# Схема для обновления (все поля опциональны, и пароль хэшируется отдельно)
class UserUpdate(BaseModel):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

# Схема, возвращаемая наружу (без пароля)
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # позволяет напрямую возвращать ORM-модель через эту схему

# Схема для логина
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
