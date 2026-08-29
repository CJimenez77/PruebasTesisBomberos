from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class TipoInspeccion(Base):
    __tablename__ = "tipo_inspeccion"

    id_tipo_inspeccion = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    inspecciones = relationship("Inspeccion", back_populates="tipo_inspeccion")


class Inspeccion(Base):
    __tablename__ = "inspeccion"

    id_inspeccion = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    id_tipo_inspeccion = Column(
        Integer,
        ForeignKey("tipo_inspeccion.id_tipo_inspeccion", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_ubicacion = Column(
        Integer,
        ForeignKey("ubicacion.id_ubicacion", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    tipo_inspeccion = relationship("TipoInspeccion", back_populates="inspecciones")
    usuario = relationship("Usuario", back_populates="inspecciones")
    ubicacion = relationship("Ubicacion", back_populates="inspecciones")
    detalles = relationship("DetalleInspeccion", back_populates="inspeccion", cascade="all, delete-orphan")


class DetalleInspeccion(Base):
    __tablename__ = "detalle_inspeccion"

    id_detalle = Column(Integer, primary_key=True, index=True)
    cantidad_encontrada = Column(Integer, nullable=False)
    cantidad_teorica_actual = Column(Integer, nullable=False)
    estado_reportado = Column(String(50), nullable=False, default="OPERATIVO")

    id_inspeccion = Column(
        Integer,
        ForeignKey("inspeccion.id_inspeccion", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    id_item = Column(
        Integer,
        ForeignKey("item.id_item", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("cantidad_encontrada >= 0", name="chk_detalle_encontrada_non_negative"),
        CheckConstraint("cantidad_teorica_actual >= 0", name="chk_detalle_teorica_non_negative"),
    )

    inspeccion = relationship("Inspeccion", back_populates="detalles")
    item = relationship("Item", back_populates="detalles_inspeccion")
    alerta = relationship("AlertaDiscrepancia", back_populates="detalle", uselist=False, cascade="all, delete-orphan")


class EstadoAlerta(Base):
    __tablename__ = "estado_alerta"

    id_estado_alerta = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)

    alertas = relationship("AlertaDiscrepancia", back_populates="estado_alerta")


class AlertaDiscrepancia(Base):
    __tablename__ = "alerta_discrepancia"

    id_alerta = Column(Integer, primary_key=True, index=True)
    fecha_generacion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    resuelta = Column(Boolean, nullable=False, default=False)
    diferencia = Column(Integer, nullable=False)  # cantidad_encontrada - cantidad_teorica_actual
    fecha_resolucion = Column(DateTime(timezone=True), nullable=True)
    observaciones = Column(Text, nullable=True)

    id_detalle = Column(
        Integer,
        ForeignKey("detalle_inspeccion.id_detalle", onupdate="CASCADE", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    id_estado_alerta = Column(
        Integer,
        ForeignKey("estado_alerta.id_estado_alerta", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    detalle = relationship("DetalleInspeccion", back_populates="alerta")
    estado_alerta = relationship("EstadoAlerta", back_populates="alertas")
    usuario_resolutor = relationship("Usuario", foreign_keys=[id_usuario])
