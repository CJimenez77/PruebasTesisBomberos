from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_voluntario = Column(Integer, nullable=True)  # FK logica modulo Personal
    nombre = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")
    movimientos = relationship("Movimiento", back_populates="usuario")
    inspecciones = relationship("Inspeccion", back_populates="usuario")
