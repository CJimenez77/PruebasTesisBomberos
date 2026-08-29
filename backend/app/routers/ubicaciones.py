from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ubicacion import AsignacionResponse, TipoUbicacionResponse, UbicacionCreate, UbicacionResponse

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones & Distribución"])


@router.get("/tipos", response_model=List[TipoUbicacionResponse])
def get_tipos_ubicacion(db: Session = Depends(get_db)):
    """Retorna los tipos maestros de ubicación (Carro bomba, Bodega, Cortina, etc.)."""
    result = db.execute(text("SELECT id_tipo_ubicacion, tipo FROM TIPO_UBICACION ORDER BY id_tipo_ubicacion")).fetchall()
    return [{"id_tipo_ubicacion": r[0], "tipo": r[1]} for r in result]


@router.get("/", response_model=List[UbicacionResponse])
def list_ubicaciones(db: Session = Depends(get_db)):
    """Lista todas las ubicaciones y carros registrados."""
    rows = db.execute(
        text("""
            SELECT u.id_ubicacion, u.nombre, u.descripcion, u.id_tipo_ubicacion, u.id_ubicacion_padre, t.tipo
            FROM UBICACION u
            JOIN TIPO_UBICACION t ON u.id_tipo_ubicacion = t.id_tipo_ubicacion
            ORDER BY u.id_ubicacion
        """)
    ).fetchall()

    return [
        {
            "id_ubicacion": r[0],
            "nombre": r[1],
            "descripcion": r[2],
            "id_tipo_ubicacion": r[3],
            "id_ubicacion_padre": r[4],
            "tipo_nombre": r[5],
            "sub_ubicaciones": [],
        }
        for r in rows
    ]


@router.post("/", response_model=UbicacionResponse, status_code=status.HTTP_201_CREATED)
def create_ubicacion(ubicacion_in: UbicacionCreate, db: Session = Depends(get_db)):
    """Crea una nueva ubicación (ej. Carro B-6 o Cortina Izquierda 1)."""
    result = db.execute(
        text("""
            INSERT INTO UBICACION (nombre, descripcion, id_tipo_ubicacion, id_ubicacion_padre)
            VALUES (:nombre, :descripcion, :id_tipo_ubicacion, :id_ubicacion_padre)
            RETURNING id_ubicacion
        """),
        {
            "nombre": ubicacion_in.nombre,
            "descripcion": ubicacion_in.descripcion,
            "id_tipo_ubicacion": ubicacion_in.id_tipo_ubicacion,
            "id_ubicacion_padre": ubicacion_in.id_ubicacion_padre,
        },
    )
    new_id = result.scalar()
    db.commit()

    tipo_row = db.execute(
        text("SELECT tipo FROM TIPO_UBICACION WHERE id_tipo_ubicacion = :id"),
        {"id": ubicacion_in.id_tipo_ubicacion},
    ).fetchone()

    return {
        "id_ubicacion": new_id,
        "nombre": ubicacion_in.nombre,
        "descripcion": ubicacion_in.descripcion,
        "id_tipo_ubicacion": ubicacion_in.id_tipo_ubicacion,
        "id_ubicacion_padre": ubicacion_in.id_ubicacion_padre,
        "tipo_nombre": tipo_row[0] if tipo_row else "",
        "sub_ubicaciones": [],
    }


@router.get("/{id_ubicacion}/stock", response_model=List[AsignacionResponse])
def get_stock_en_ubicacion(id_ubicacion: int, db: Session = Depends(get_db)):
    """Retorna el inventario actual asignado a una ubicación específica."""
    rows = db.execute(
        text("""
            SELECT a.id_item, a.id_ubicacion, i.nombre as item_nombre, u.nombre as ubicacion_nombre, 
                   a.cantidad_asignada, a.fecha
            FROM ASIGNACION_ITEMS a
            JOIN ITEM i ON a.id_item = i.id_item
            JOIN UBICACION u ON a.id_ubicacion = u.id_ubicacion
            WHERE a.id_ubicacion = :id_ubicacion
            ORDER BY i.nombre
        """),
        {"id_ubicacion": id_ubicacion},
    ).fetchall()

    return [
        {
            "id_item": r[0],
            "id_ubicacion": r[1],
            "item_nombre": r[2],
            "ubicacion_nombre": r[3],
            "cantidad_asignada": r[4],
            "fecha": r[5],
        }
        for r in rows
    ]
