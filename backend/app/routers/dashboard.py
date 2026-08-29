from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Métricas"])


@router.get("/resumen")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Retorna métricas consolidadas del cuartel para el Directorio y Mando."""
    total_items = db.execute(text("SELECT COUNT(*) FROM ITEM")).scalar()
    total_unidades_stock = db.execute(text("SELECT COALESCE(SUM(cantidad), 0) FROM ITEM")).scalar()
    total_carros = db.execute(text("SELECT COUNT(*) FROM UBICACION WHERE id_tipo_ubicacion = 1")).scalar()
    alertas_pendientes = db.execute(text("SELECT COUNT(*) FROM ALERTA_DISCREPANCIA WHERE resuelta = FALSE")).scalar()
    inspecciones_count = db.execute(text("SELECT COUNT(*) FROM INSPECCION")).scalar()

    # Obtener últimas alertas activas
    ultimas_alertas = db.execute(
        text("""
            SELECT a.id_alerta, i.nombre as item_nombre, ub.nombre as ubicacion_nombre, 
                   a.diferencia, a.observaciones, a.fecha_generacion
            FROM ALERTA_DISCREPANCIA a
            JOIN DETALLE_INSPECCION d ON a.id_detalle = d.id_detalle
            JOIN INSPECCION ins ON d.id_inspeccion = ins.id_inspeccion
            JOIN UBICACION ub ON ins.id_ubicacion = ub.id_ubicacion
            JOIN ITEM i ON d.id_item = i.id_item
            WHERE a.resuelta = FALSE
            ORDER BY a.fecha_generacion DESC
            LIMIT 5
        """)
    ).fetchall()

    return {
        "total_items": total_items,
        "total_unidades_stock": total_unidades_stock,
        "total_carros": total_carros,
        "alertas_pendientes": alertas_pendientes,
        "inspecciones_count": inspecciones_count,
        "ultimas_alertas": [
            {
                "id_alerta": r[0],
                "item_nombre": r[1],
                "ubicacion_nombre": r[2],
                "diferencia": r[3],
                "observaciones": r[4],
                "fecha_generacion": r[5],
            }
            for r in ultimas_alertas
        ],
    }
