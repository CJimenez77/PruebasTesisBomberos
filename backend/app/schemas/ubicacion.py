from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TipoUbicacionResponse(BaseModel):
    id_tipo_ubicacion: int
    tipo: str

    class Config:
        from_attributes = True


class UbicacionBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    id_tipo_ubicacion: int
    id_ubicacion_padre: Optional[int] = None


class UbicacionCreate(UbicacionBase):
    pass


class UbicacionResponse(UbicacionBase):
    id_ubicacion: int
    tipo_nombre: Optional[str] = None
    sub_ubicaciones: List["UbicacionResponse"] = []

    class Config:
        from_attributes = True


class AsignacionCreate(BaseModel):
    id_item: int
    id_ubicacion: int
    cantidad_asignada: int = Field(1, ge=0)


class AsignacionResponse(BaseModel):
    id_item: int
    id_ubicacion: int
    item_nombre: Optional[str] = None
    ubicacion_nombre: Optional[str] = None
    cantidad_asignada: int
    fecha: datetime

    class Config:
        from_attributes = True
