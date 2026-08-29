from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class TipoUbicacion(Base):
    __tablename__ = "tipo_ubicacion"

    id_tipo_ubicacion = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), unique=True, nullable=False)

    ubicaciones = relationship("Ubicacion", back_populates="tipo_ubicacion")


class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id_ubicacion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    id_tipo_ubicacion = Column(
        Integer,
        ForeignKey("tipo_ubicacion.id_tipo_ubicacion", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_ubicacion_padre = Column(
        Integer,
        ForeignKey("ubicacion.id_ubicacion", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    tipo_ubicacion = relationship("TipoUbicacion", back_populates="ubicaciones")

    # Relación Reflexiva Cíclica (Jerarquía Padre -> Hijos)
    sub_ubicaciones = relationship("Ubicacion", backref="ubicacion_padre", remote_side=[id_ubicacion])

    asignaciones = relationship("AsignacionItems", back_populates="ubicacion")
    inspecciones = relationship("Inspeccion", back_populates="ubicacion")


class AsignacionItems(Base):
    __tablename__ = "asignacion_items"

    id_item = Column(
        Integer,
        ForeignKey("item.id_item", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    id_ubicacion = Column(
        Integer,
        ForeignKey("ubicacion.id_ubicacion", onupdate="CASCADE", ondelete="RESTRICT"),
        primary_key=True,
    )
    cantidad_asignada = Column(Integer, nullable=False, default=1)
    fecha = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (CheckConstraint("cantidad_asignada >= 0", name="chk_asignacion_cantidad_non_negative"),)

    item = relationship("Item", back_populates="asignaciones")
    ubicacion = relationship("Ubicacion", back_populates="asignaciones")
