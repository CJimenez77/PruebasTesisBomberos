import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import engine, get_db
from app.routers import auth, catalogo, dashboard, inspecciones, movimientos, ubicaciones


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cargar y ejecutar init-db.sql o DDL al iniciar
    try:
        init_sql_path = os.path.join(os.path.dirname(__file__), "..", "..", "init-db.sql")
        if os.path.exists(init_sql_path):
            with open(init_sql_path, "r", encoding="utf-8") as f:
                ddl_content = f.read()
            with engine.connect() as conn:
                conn.execute(text(ddl_content))
                conn.commit()
                print("Base de datos MER v3 y dataset sintetico cargados exitosamente desde init-db.sql.")
    except Exception as e:
        print(f"Aviso inicializando BD: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "API REST Oficial para el Módulo de Inventarios y Trazabilidad Operativa "
        "(Proyecto de Título UBB - Cristian Jiménez & Matías Aguilera)"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS habilitado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Routers de la API v1
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(catalogo.router, prefix=settings.API_V1_STR)
app.include_router(ubicaciones.router, prefix=settings.API_V1_STR)
app.include_router(movimientos.router, prefix=settings.API_V1_STR)
app.include_router(inspecciones.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)


@app.get("/", tags=["General"])
def root():
    return {
        "sistema": "Módulo de Gestión de Inventarios - Sexta Compañía de Bomberos",
        "estado": "Operativo",
        "ambiente": "Staging (Cloud)",
        "documentacion": "/docs",
        "autores": ["Cristian Jiménez", "Matías Aguilera"],
    }


@app.get("/api/v1/health", tags=["Salud & Diagnóstico"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        roles_count = db.execute(text("SELECT COUNT(*) FROM ROL")).scalar()
        categorias_count = db.execute(text("SELECT COUNT(*) FROM CATEGORIA_ITEM")).scalar()
        items_count = db.execute(text("SELECT COUNT(*) FROM ITEM")).scalar()
        ubicaciones_count = db.execute(text("SELECT COUNT(*) FROM UBICACION")).scalar()

        return {
            "status": "HEALTHY",
            "database": "CONNECTED",
            "engine": "PostgreSQL 16",
            "seed_data": {
                "roles_cargados": roles_count,
                "categorias_cargadas": categorias_count,
                "items_cargados": items_count,
                "ubicaciones_cargadas": ubicaciones_count,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error conectando a la base de datos: {e!s}",
        ) from e
