from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.schemas.inspeccion import (
    AlertaResolverRequest,
    AlertaResponse,
    EstadoAlertaResponse,
    InspeccionCreate,
    InspeccionResponse,
    TipoInspeccionResponse,
)

router = APIRouter(prefix="/inspecciones", tags=["Inspecciones & Alertas de Discrepancia"])


@router.get("/tipos", response_model=List[TipoInspeccionResponse])
def get_tipos_inspeccion(db: Session = Depends(get_db)):
    """Retorna los tipos maestros de inspección (Rutinaria vs Post-Emergencia)."""
    rows = db.execute(text("SELECT id_tipo_inspeccion, nombre, descripcion FROM TIPO_INSPECCION ORDER BY id_tipo_inspeccion")).fetchall()
    return [{"id_tipo_inspeccion": r[0], "nombre": r[1], "descripcion": r[2]} for r in rows]


@router.get("/estados-alerta", response_model=List[EstadoAlertaResponse])
def get_estados_alerta(db: Session = Depends(get_db)):
    """Retorna los estados posibles para la resolución de alertas de discrepancia."""
    rows = db.execute(text("SELECT id_estado_alerta, nombre, descripcion FROM ESTADO_ALERTA ORDER BY id_estado_alerta")).fetchall()
    return [{"id_estado_alerta": r[0], "nombre": r[1], "descripcion": r[2]} for r in rows]


@router.get("/", response_model=List[InspeccionResponse])
def list_inspecciones(
    id_ubicacion: Optional[int] = Query(default=None, description="Filtrar por carro o ubicación"),
    limit: int = Query(default=30, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lista las inspecciones realizadas en terreno con sus respectivos detalles."""
    query = """
        SELECT i.id_inspeccion, i.id_tipo_inspeccion, ti.nombre as tipo_nombre,
               i.id_usuario, u.nombre as usuario_nombre,
               i.id_ubicacion, ub.nombre as ubicacion_nombre, i.fecha
        FROM INSPECCION i
        JOIN TIPO_INSPECCION ti ON i.id_tipo_inspeccion = ti.id_tipo_inspeccion
        JOIN USUARIO u ON i.id_usuario = u.id_usuario
        JOIN UBICACION ub ON i.id_ubicacion = ub.id_ubicacion
        WHERE 1=1
    """
    params = {}
    if id_ubicacion:
        query += " AND i.id_ubicacion = :id_ubicacion"
        params["id_ubicacion"] = id_ubicacion

    query += " ORDER BY i.fecha DESC LIMIT :limit"
    params["limit"] = limit

    inspecciones_rows = db.execute(text(query), params).fetchall()
    resultado = []

    for ins in inspecciones_rows:
        detalles_rows = db.execute(
            text("""
                SELECT d.id_detalle, d.id_item, it.nombre as item_nombre,
                       d.cantidad_encontrada, d.cantidad_teorica_actual, d.estado_reportado
                FROM DETALLE_INSPECCION d
                JOIN ITEM it ON d.id_item = it.id_item
                WHERE d.id_inspeccion = :id_ins
            """),
            {"id_ins": ins[0]},
        ).fetchall()

        detalles = [
            {
                "id_detalle": d[0],
                "id_item": d[1],
                "item_nombre": d[2],
                "cantidad_encontrada": d[3],
                "cantidad_teorica_actual": d[4],
                "estado_reportado": d[5],
            }
            for d in detalles_rows
        ]

        resultado.append(
            {
                "id_inspeccion": ins[0],
                "id_tipo_inspeccion": ins[1],
                "tipo_nombre": ins[2],
                "id_usuario": ins[3],
                "usuario_nombre": ins[4],
                "id_ubicacion": ins[5],
                "ubicacion_nombre": ins[6],
                "fecha": ins[7],
                "detalles": detalles,
            }
        )

    return resultado


@router.post("/", response_model=InspeccionResponse, status_code=status.HTTP_201_CREATED)
def create_inspeccion(
    insp_in: InspeccionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Registra una inspección de terreno.
    Si se detecta cualquier diferencia entre stock encontrado y teórico, 
    crea automáticamente una ALERTA_DISCREPANCIA en estado PENDIENTE.
    """
    # 1. Crear cabecera de inspección
    res_insp = db.execute(
        text("""
            INSERT INTO INSPECCION (id_tipo_inspeccion, id_usuario, id_ubicacion, fecha)
            VALUES (:tipo, :usuario, :ubicacion, NOW())
            RETURNING id_inspeccion
        """),
        {
            "tipo": insp_in.id_tipo_inspeccion,
            "usuario": current_user["id_usuario"],
            "ubicacion": insp_in.id_ubicacion,
        },
    )
    id_inspeccion = res_insp.scalar()

    # 2. Insertar detalles y generar alertas si aplica
    for det in insp_in.detalles:
        res_det = db.execute(
            text("""
                INSERT INTO DETALLE_INSPECCION (cantidad_encontrada, cantidad_teorica_actual, estado_reportado, id_inspeccion, id_item)
                VALUES (:encontrada, :teorica, :estado, :id_ins, :id_item)
                RETURNING id_detalle
            """),
            {
                "encontrada": det.cantidad_encontrada,
                "teorica": det.cantidad_teorica_actual,
                "estado": det.estado_reportado,
                "id_ins": id_inspeccion,
                "id_item": det.id_item,
            },
        )
        id_detalle = res_det.scalar()

        # Detección de discrepancia
        diferencia = det.cantidad_encontrada - det.cantidad_teorica_actual
        if diferencia != 0:
            item_nombre = db.execute(
                text("SELECT nombre FROM ITEM WHERE id_item = :id"),
                {"id": det.id_item},
            ).scalar()
            obs = f"Discrepancia detectada en inspección: {abs(diferencia)} unidad(es) de '{item_nombre}' " + (
                "faltante(s)" if diferencia < 0 else "sobrante(s)"
            )

            db.execute(
                text("""
                    INSERT INTO ALERTA_DISCREPANCIA (id_detalle, id_estado_alerta, diferencia, resuelta, observaciones, fecha_generacion)
                    VALUES (:id_det, 1, :dif, FALSE, :obs, NOW())
                """),
                {
                    "id_det": id_detalle,
                    "dif": diferencia,
                    "obs": obs,
                },
            )

    db.commit()

    # Retornar la inspección recién creada
    return list_inspecciones(id_ubicacion=insp_in.id_ubicacion, limit=1, db=db)[0]


@router.get("/alertas", response_model=List[AlertaResponse])
def list_alertas(
    solo_pendientes: bool = Query(default=False, description="Filtrar solo alertas no resueltas"),
    db: Session = Depends(get_db),
):
    """Lista las alertas de discrepancia registradas en el sistema."""
    query = """
        SELECT a.id_alerta, a.id_detalle, i.nombre as item_nombre, ub.nombre as ubicacion_nombre,
               a.diferencia, a.resuelta, a.id_estado_alerta, ea.nombre as estado_nombre,
               a.fecha_generacion, a.fecha_resolucion, a.observaciones,
               a.id_usuario, u.nombre as usuario_resolutor_nombre
        FROM ALERTA_DISCREPANCIA a
        JOIN DETALLE_INSPECCION d ON a.id_detalle = d.id_detalle
        JOIN INSPECCION ins ON d.id_inspeccion = ins.id_inspeccion
        JOIN UBICACION ub ON ins.id_ubicacion = ub.id_ubicacion
        JOIN ITEM i ON d.id_item = i.id_item
        JOIN ESTADO_ALERTA ea ON a.id_estado_alerta = ea.id_estado_alerta
        LEFT JOIN USUARIO u ON a.id_usuario = u.id_usuario
        WHERE 1=1
    """
    if solo_pendientes:
        query += " AND a.resuelta = FALSE"

    query += " ORDER BY a.fecha_generacion DESC"
    rows = db.execute(text(query)).fetchall()

    return [
        {
            "id_alerta": r[0],
            "id_detalle": r[1],
            "item_nombre": r[2],
            "ubicacion_nombre": r[3],
            "diferencia": r[4],
            "resuelta": r[5],
            "id_estado_alerta": r[6],
            "estado_nombre": r[7],
            "fecha_generacion": r[8],
            "fecha_resolucion": r[9],
            "observaciones": r[10],
            "id_usuario": r[11],
            "usuario_resolutor_nombre": r[12],
        }
        for r in rows
    ]


@router.post("/alertas/{id_alerta}/resolver", response_model=AlertaResponse)
def resolver_alerta(
    id_alerta: int,
    resolucion: AlertaResolverRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Permite al Director o Capitán visar y cerrar una alerta de discrepancia.
    Registra el oficial responsable, estado definitivo y observaciones.
    """
    alerta_row = db.execute(
        text("SELECT id_alerta FROM ALERTA_DISCREPANCIA WHERE id_alerta = :id"),
        {"id": id_alerta},
    ).fetchone()

    if not alerta_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alerta no encontrada")

    db.execute(
        text("""
            UPDATE ALERTA_DISCREPANCIA
            SET resuelta = TRUE,
                id_estado_alerta = :estado,
                id_usuario = :usuario,
                observaciones = :obs,
                fecha_resolucion = NOW()
            WHERE id_alerta = :id
        """),
        {
            "estado": resolucion.id_estado_alerta,
            "usuario": current_user["id_usuario"],
            "obs": resolucion.observaciones,
            "id": id_alerta,
        },
    )
    db.commit()

    return [a for a in list_alertas(db=db) if a["id_alerta"] == id_alerta][0]
