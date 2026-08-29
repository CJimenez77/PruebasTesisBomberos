from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class TipoMovimiento(Base):
    __tablename__ = "tipo_movimiento"

    id_tipo_mov = Column(Integer, primary_key=True, index=True)
    tipo_mov = Column(String(50), unique=True, nullable=False)

    movimientos = relationship("Movimiento", back_populates="tipo_movimiento")


class Movimiento(Base):
    __tablename__ = "movimiento"

    id_movimiento = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    fecha = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    observaciones = Column(Text, nullable=True)

    id_tipo_mov = Column(
        Integer,
        ForeignKey("tipo_movimiento.id_tipo_mov", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_item = Column(
        Integer,
        ForeignKey("item.id_item", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_usuario = Column(
        Integer,
        ForeignKey("usuario.id_usuario", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_ubicacion_origen = Column(
        Integer,
        ForeignKey("ubicacion.id_ubicacion", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    id_ubicacion_destino = Column(
        Integer,
        ForeignKey("ubicacion.id_ubicacion", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    __table_args__ = (CheckConstraint("cantidad > 0", name="chk_movimiento_cantidad_positive"),)

    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    item = relationship("Item", back_populates="movimientos")
    usuario = relationship("Usuario", back_populates="movimientos")
    ubicacion_origen = relationship("Ubicacion", foreign_keys=[id_ubicacion_origen])
    ubicacion_destino = relationship("Ubicacion", foreign_keys=[id_ubicacion_destino])
