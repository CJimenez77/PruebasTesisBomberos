from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class CategoriaItem(Base):
    __tablename__ = "categoria_item"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)

    items = relationship("Item", back_populates="categoria")


class TipoItem(Base):
    __tablename__ = "tipo_item"

    id_tipo_item = Column(Integer, primary_key=True, index=True)
    tipo_clasificacion = Column(String(50), unique=True, nullable=False)  # 'AGRUPABLE_LOTE' vs 'UNITARIO_ETIQUETABLE'

    items = relationship("Item", back_populates="tipo_item")


class Item(Base):
    __tablename__ = "item"

    id_item = Column(Integer, primary_key=True, index=True)
    codigo_qr = Column(String(100), unique=True, nullable=True, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(String(50), nullable=False, default="OPERATIVO")  # 'OPERATIVO', 'EN_MANTENCION', 'DANADO', etc.
    cantidad = Column(Integer, nullable=False, default=1)
    fecha_vencimiento = Column(Date, nullable=True)
    id_categoria = Column(
        Integer,
        ForeignKey("categoria_item.id_categoria", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    id_tipo_item = Column(
        Integer,
        ForeignKey("tipo_item.id_tipo_item", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    __table_args__ = (CheckConstraint("cantidad >= 0", name="chk_item_cantidad_non_negative"),)

    categoria = relationship("CategoriaItem", back_populates="items")
    tipo_item = relationship("TipoItem", back_populates="items")
    asignaciones = relationship("AsignacionItems", back_populates="item", cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="item")
    detalles_inspeccion = relationship("DetalleInspeccion", back_populates="item")
