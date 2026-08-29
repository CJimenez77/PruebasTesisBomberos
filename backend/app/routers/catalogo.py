from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.catalogo import CategoriaResponse, ItemCreate, ItemResponse, TipoItemResponse

router = APIRouter(prefix="/catalogo", tags=["Catálogo de Bienes"])


@router.get("/categorias", response_model=List[CategoriaResponse])
def get_categorias(db: Session = Depends(get_db)):
    """Retorna todas las categorías maestras de bienes."""
    result = db.execute(text("SELECT id_categoria, nombre FROM CATEGORIA_ITEM ORDER BY id_categoria")).fetchall()
    return [{"id_categoria": r[0], "nombre": r[1]} for r in result]


@router.get("/tipos-item", response_model=List[TipoItemResponse])
def get_tipos_item(db: Session = Depends(get_db)):
    """Retorna los tipos de clasificación (Agrupable vs Unitario QR)."""
    result = db.execute(text("SELECT id_tipo_item, tipo_clasificacion FROM TIPO_ITEM ORDER BY id_tipo_item")).fetchall()
    return [{"id_tipo_item": r[0], "tipo_clasificacion": r[1]} for r in result]


@router.get("/items", response_model=List[ItemResponse])
def list_items(
    id_categoria: Optional[int] = Query(None, description="Filtrar por categoría"),
    id_tipo_item: Optional[int] = Query(None, description="Filtrar por tipo (Agrupable vs QR)"),
    codigo_qr: Optional[str] = Query(None, description="Buscar por código QR exacto"),
    q: Optional[str] = Query(None, description="Búsqueda por texto en nombre o descripción"),
    db: Session = Depends(get_db),
):
    """Listado dinámico de bienes en catálogo con filtros opcionales."""
    query = """
        SELECT i.id_item, i.codigo_qr, i.nombre, i.descripcion, i.estado, i.cantidad, 
               i.fecha_vencimiento, i.id_categoria, i.id_tipo_item,
               c.nombre as categoria_nombre, t.tipo_clasificacion
        FROM ITEM i
        JOIN CATEGORIA_ITEM c ON i.id_categoria = c.id_categoria
        JOIN TIPO_ITEM t ON i.id_tipo_item = t.id_tipo_item
        WHERE 1=1
    """
    params = {}

    if id_categoria:
        query += " AND i.id_categoria = :id_categoria"
        params["id_categoria"] = id_categoria
    if id_tipo_item:
        query += " AND i.id_tipo_item = :id_tipo_item"
        params["id_tipo_item"] = id_tipo_item
    if codigo_qr:
        query += " AND i.codigo_qr = :codigo_qr"
        params["codigo_qr"] = codigo_qr
    if q:
        query += " AND (i.nombre ILIKE :q OR i.descripcion ILIKE :q)"
        params["q"] = f"%{q}%"

    query += " ORDER BY i.id_item"
    rows = db.execute(text(query), params).fetchall()

    return [
        {
            "id_item": r[0],
            "codigo_qr": r[1],
            "nombre": r[2],
            "descripcion": r[3],
            "estado": r[4],
            "cantidad": r[5],
            "fecha_vencimiento": r[6],
            "id_categoria": r[7],
            "id_tipo_item": r[8],
            "categoria_nombre": r[9],
            "tipo_clasificacion": r[10],
        }
        for r in rows
    ]


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
):
    """
    Registra un nuevo bien en el catálogo institucional.
    Valida que los ítems unitarios (QR) no tengan código duplicado.
    """
    # Verificar código QR único si aplica
    if item_in.codigo_qr:
        exists = db.execute(
            text("SELECT id_item FROM ITEM WHERE codigo_qr = :qr"),
            {"qr": item_in.codigo_qr},
        ).fetchone()
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un ítem registrado con el código QR: {item_in.codigo_qr}",
            )

    insert_query = text("""
        INSERT INTO ITEM (nombre, descripcion, codigo_qr, estado, cantidad, fecha_vencimiento, id_categoria, id_tipo_item)
        VALUES (:nombre, :descripcion, :codigo_qr, :estado, :cantidad, :fecha_vencimiento, :id_categoria, :id_tipo_item)
        RETURNING id_item
    """)

    db.execute(
        insert_query,
        {
            "nombre": item_in.nombre,
            "descripcion": item_in.descripcion,
            "codigo_qr": item_in.codigo_qr,
            "estado": item_in.estado,
            "cantidad": item_in.cantidad,
            "fecha_vencimiento": item_in.fecha_vencimiento,
            "id_categoria": item_in.id_categoria,
            "id_tipo_item": item_in.id_tipo_item,
        },
    )
    db.commit()

    # Retornar item completo
    return list_items(q=item_in.nombre, db=db)[0]


@router.get("/items/{id_item}", response_model=ItemResponse)
def get_item_by_id(id_item: int, db: Session = Depends(get_db)):
    """Obtiene el detalle de un ítem por su identificador primario."""
    row = db.execute(
        text("""
            SELECT i.id_item, i.codigo_qr, i.nombre, i.descripcion, i.estado, i.cantidad, 
                   i.fecha_vencimiento, i.id_categoria, i.id_tipo_item,
                   c.nombre as categoria_nombre, t.tipo_clasificacion
            FROM ITEM i
            JOIN CATEGORIA_ITEM c ON i.id_categoria = c.id_categoria
            JOIN TIPO_ITEM t ON i.id_tipo_item = t.id_tipo_item
            WHERE i.id_item = :id_item
        """),
        {"id_item": id_item},
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró el ítem con ID {id_item}",
        )

    return {
        "id_item": row[0],
        "codigo_qr": row[1],
        "nombre": row[2],
        "descripcion": row[3],
        "estado": row[4],
        "cantidad": row[5],
        "fecha_vencimiento": row[6],
        "id_categoria": row[7],
        "id_tipo_item": row[8],
        "categoria_nombre": row[9],
        "tipo_clasificacion": row[10],
    }
