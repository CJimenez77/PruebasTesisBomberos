from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre: str

    class Config:
        from_attributes = True


class TipoItemResponse(BaseModel):
    id_tipo_item: int
    tipo_clasificacion: str

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    descripcion: Optional[str] = None
    codigo_qr: Optional[str] = None
    estado: str = "OPERATIVO"
    cantidad: int = Field(1, ge=0)
    fecha_vencimiento: Optional[date] = None
    id_categoria: int
    id_tipo_item: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=150)
    descripcion: Optional[str] = None
    codigo_qr: Optional[str] = None
    estado: Optional[str] = None
    cantidad: Optional[int] = Field(None, ge=0)
    fecha_vencimiento: Optional[date] = None
    id_categoria: Optional[int] = None
    id_tipo_item: Optional[int] = None


class ItemResponse(ItemBase):
    id_item: int
    categoria_nombre: Optional[str] = None
    tipo_clasificacion: Optional[str] = None

    class Config:
        from_attributes = True
