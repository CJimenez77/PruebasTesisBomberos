from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TipoMovimientoResponse(BaseModel):
    id_tipo_mov: int
    tipo_mov: str

    class Config:
        from_attributes = True


class MovimientoCreate(BaseModel):
    id_item: int
    id_tipo_mov: int
    cantidad: int = Field(..., gt=0)
    id_ubicacion_origen: Optional[int] = None
    id_ubicacion_destino: Optional[int] = None
    observaciones: Optional[str] = None


class MovimientoResponse(BaseModel):
    id_movimiento: int
    id_item: int
    item_nombre: Optional[str] = None
    id_usuario: int
    usuario_nombre: Optional[str] = None
    id_tipo_mov: int
    tipo_movimiento_nombre: Optional[str] = None
    id_ubicacion_origen: Optional[int] = None
    origen_nombre: Optional[str] = None
    id_ubicacion_destino: Optional[int] = None
    destino_nombre: Optional[str] = None
    cantidad: int
    fecha: datetime
    observaciones: Optional[str] = None

    class Config:
        from_attributes = True
