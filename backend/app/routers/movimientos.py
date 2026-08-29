from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.schemas.movimiento import MovimientoCreate, MovimientoResponse, TipoMovimientoResponse

router = APIRouter(prefix="/movimientos", tags=["Movimientos & Ledger Inmutable"])


def fetch_movimiento_by_id(id_movimiento: int, db: Session) -> dict | None:
    query = """
        SELECT m.id_movimiento, m.id_item, i.nombre as item_nombre,
               m.id_usuario, u.nombre as usuario_nombre,
               m.id_tipo_mov, tm.tipo_mov as tipo_movimiento_nombre,
               m.id_ubicacion_origen, uo.nombre as origen_nombre,
               m.id_ubicacion_destino, ud.nombre as destino_nombre,
               m.cantidad, m.fecha, m.observaciones
        FROM MOVIMIENTO m
        JOIN ITEM i ON m.id_item = i.id_item
        JOIN USUARIO u ON m.id_usuario = u.id_usuario
        JOIN TIPO_MOVIMIENTO tm ON m.id_tipo_mov = tm.id_tipo_mov
        LEFT JOIN UBICACION uo ON m.id_ubicacion_origen = uo.id_ubicacion
        LEFT JOIN UBICACION ud ON m.id_ubicacion_destino = ud.id_ubicacion
        WHERE m.id_movimiento = :id_mov
    """
    r = db.execute(text(query), {"id_mov": id_movimiento}).fetchone()
    if not r:
        return None
    return {
        "id_movimiento": r[0],
        "id_item": r[1],
        "item_nombre": r[2],
        "id_usuario": r[3],
        "usuario_nombre": r[4],
        "id_tipo_mov": r[5],
        "tipo_movimiento_nombre": r[6],
        "id_ubicacion_origen": r[7],
        "origen_nombre": r[8],
        "id_ubicacion_destino": r[9],
        "destino_nombre": r[10],
        "cantidad": r[11],
        "fecha": r[12],
        "observaciones": r[13],
    }


@router.get("/tipos", response_model=List[TipoMovimientoResponse])
def get_tipos_movimiento(db: Session = Depends(get_db)):
    """Retorna los tipos maestros de movimiento del sistema."""
    rows = db.execute(text("SELECT id_tipo_mov, tipo_mov FROM TIPO_MOVIMIENTO ORDER BY id_tipo_mov")).fetchall()
    return [{"id_tipo_mov": r[0], "tipo_mov": r[1]} for r in rows]


@router.get("/", response_model=List[MovimientoResponse])
def list_movimientos(
    id_item: Optional[int] = Query(default=None, description="Filtrar por ítem"),
    id_ubicacion: Optional[int] = Query(default=None, description="Filtrar por ubicación origen o destino"),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Retorna el historial inmutable de movimientos auditados."""
    query = """
        SELECT m.id_movimiento
        FROM MOVIMIENTO m
        WHERE 1=1
    """
    params = {}
    if id_item:
        query += " AND m.id_item = :id_item"
        params["id_item"] = id_item
    if id_ubicacion:
        query += " AND (m.id_ubicacion_origen = :id_ubicacion OR m.id_ubicacion_destino = :id_ubicacion)"
        params["id_ubicacion"] = id_ubicacion

    query += " ORDER BY m.fecha DESC LIMIT :limit"
    params["limit"] = limit

    rows = db.execute(text(query), params).fetchall()
    return [fetch_movimiento_by_id(r[0], db=db) for r in rows]


@router.post("/", response_model=MovimientoResponse, status_code=status.HTTP_201_CREATED)
def create_movimiento(
    mov_in: MovimientoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Registra un movimiento en el ledger inmutable y actualiza el saldo físico en ASIGNACION_ITEMS.
    Soporta traslados entre ubicaciones, compras (origen NULL), bajas (destino NULL) y recuperaciones.
    """
    # 1. Si hay ubicación de origen, validar que exista stock suficiente
    if mov_in.id_ubicacion_origen:
        stock_origen_row = db.execute(
            text("SELECT cantidad_asignada FROM ASIGNACION_ITEMS WHERE id_item = :item AND id_ubicacion = :ub"),
            {"item": mov_in.id_item, "ub": mov_in.id_ubicacion_origen},
        ).fetchone()

        stock_actual = stock_origen_row[0] if stock_origen_row else 0
        if stock_actual < mov_in.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Stock insuficiente en la ubicación de origen. "
                    f"Disponible: {stock_actual}, Solicitado: {mov_in.cantidad}"
                ),
            )

        # Descontar del origen
        nuevo_stock_origen = stock_actual - mov_in.cantidad
        if nuevo_stock_origen > 0:
            db.execute(
                text("""
                    UPDATE ASIGNACION_ITEMS 
                    SET cantidad_asignada = :cant, fecha = NOW() 
                    WHERE id_item = :item AND id_ubicacion = :ub
                """),
                {"cant": nuevo_stock_origen, "item": mov_in.id_item, "ub": mov_in.id_ubicacion_origen},
            )
        else:
            db.execute(
                text("DELETE FROM ASIGNACION_ITEMS WHERE id_item = :item AND id_ubicacion = :ub"),
                {"item": mov_in.id_item, "ub": mov_in.id_ubicacion_origen},
            )

    # 2. Si hay ubicación de destino, sumar al saldo de destino
    if mov_in.id_ubicacion_destino:
        db.execute(
            text("""
                INSERT INTO ASIGNACION_ITEMS (id_item, id_ubicacion, cantidad_asignada, fecha)
                VALUES (:item, :ub, :cant, NOW())
                ON CONFLICT (id_item, id_ubicacion) DO UPDATE
                SET cantidad_asignada = ASIGNACION_ITEMS.cantidad_asignada + EXCLUDED.cantidad_asignada,
                    fecha = NOW()
            """),
            {"item": mov_in.id_item, "ub": mov_in.id_ubicacion_destino, "cant": mov_in.cantidad},
        )

    # 3. Registrar el movimiento en el Ledger inmutable
    res = db.execute(
        text("""
            INSERT INTO MOVIMIENTO (cantidad, id_tipo_mov, id_item, id_usuario, id_ubicacion_origen, id_ubicacion_destino, observaciones, fecha)
            VALUES (:cantidad, :id_tipo_mov, :id_item, :id_usuario, :id_origen, :id_destino, :obs, NOW())
            RETURNING id_movimiento
        """),
        {
            "cantidad": mov_in.cantidad,
            "id_tipo_mov": mov_in.id_tipo_mov,
            "id_item": mov_in.id_item,
            "id_usuario": current_user["id_usuario"],
            "id_origen": mov_in.id_ubicacion_origen,
            "id_destino": mov_in.id_ubicacion_destino,
            "obs": mov_in.observaciones,
        },
    )
    new_id = res.scalar()
    db.commit()

    return fetch_movimiento_by_id(new_id, db=db)
