from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TipoInspeccionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_tipo_inspeccion: int
    nombre: str
    descripcion: Optional[str] = None


class EstadoAlertaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_estado_alerta: int
    nombre: str
    descripcion: Optional[str] = None


class DetalleInspeccionCreate(BaseModel):
    id_item: int
    cantidad_encontrada: int = Field(..., ge=0)
    cantidad_teorica_actual: int = Field(..., ge=0)
    estado_reportado: str = "OPERATIVO"


class DetalleInspeccionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_detalle: int
    id_item: int
    item_nombre: Optional[str] = None
    cantidad_encontrada: int
    cantidad_teorica_actual: int
    estado_reportado: str


class InspeccionCreate(BaseModel):
    id_tipo_inspeccion: int
    id_ubicacion: int
    detalles: List[DetalleInspeccionCreate]


class InspeccionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_inspeccion: int
    id_tipo_inspeccion: int
    tipo_nombre: Optional[str] = None
    id_usuario: int
    usuario_nombre: Optional[str] = None
    id_ubicacion: int
    ubicacion_nombre: Optional[str] = None
    fecha: datetime
    detalles: List[DetalleInspeccionResponse] = []


class AlertaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_alerta: int
    id_detalle: int
    item_nombre: Optional[str] = None
    ubicacion_nombre: Optional[str] = None
    diferencia: int
    resuelta: bool
    id_estado_alerta: int
    estado_nombre: Optional[str] = None
    fecha_generacion: datetime
    fecha_resolucion: Optional[datetime] = None
    observaciones: Optional[str] = None
    id_usuario: Optional[int] = None
    usuario_resolutor_nombre: Optional[str] = None


class AlertaResolverRequest(BaseModel):
    id_estado_alerta: int
    observaciones: str = Field(..., min_length=5)
