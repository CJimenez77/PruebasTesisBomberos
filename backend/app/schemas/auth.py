from typing import Optional
from pydantic import BaseModel, EmailStr


class RolResponse(BaseModel):
    id_rol: int
    nombre: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    nombre: Optional[str] = None
    id_voluntario: Optional[int] = None
    id_rol: int


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id_usuario: int
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    id_voluntario: Optional[int] = None
    id_rol: int
    role_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    user_name: Optional[str] = None


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
