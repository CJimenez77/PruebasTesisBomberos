from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import engine, get_db
from app.routers import auth, catalogo, ubicaciones

# Script DDL integrado del MER v3 para inicializacion automatica
DDL_MER_V3 = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS ROL (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    id_voluntario INT NULL,
    nombre VARCHAR(100) NULL,
    email VARCHAR(100) NULL UNIQUE,
    id_rol INT NOT NULL REFERENCES ROL(id_rol) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS CATEGORIA_ITEM (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_ITEM (
    id_tipo_item SERIAL PRIMARY KEY,
    tipo_clasificacion VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_UBICACION (
    id_tipo_ubicacion SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_MOVIMIENTO (
    id_tipo_mov SERIAL PRIMARY KEY,
    tipo_mov VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_INSPECCION (
    id_tipo_inspeccion SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT NULL
);

CREATE TABLE IF NOT EXISTS ESTADO_ALERTA (
    id_estado_alerta SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT NULL
);

CREATE TABLE IF NOT EXISTS UBICACION (
    id_ubicacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    id_tipo_ubicacion INT NOT NULL REFERENCES TIPO_UBICACION(id_tipo_ubicacion) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ubicacion_padre INT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ITEM (
    id_item SERIAL PRIMARY KEY,
    codigo_qr VARCHAR(100) NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'OPERATIVO',
    cantidad INT NOT NULL DEFAULT 1 CHECK (cantidad >= 0),
    fecha_vencimiento DATE NULL,
    id_categoria INT NOT NULL REFERENCES CATEGORIA_ITEM(id_categoria) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_tipo_item INT NOT NULL REFERENCES TIPO_ITEM(id_tipo_item) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ASIGNACION_ITEMS (
    id_item INT NOT NULL REFERENCES ITEM(id_item) ON UPDATE CASCADE ON DELETE CASCADE,
    id_ubicacion INT NOT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE RESTRICT,
    cantidad_asignada INT NOT NULL DEFAULT 1 CHECK (cantidad_asignada >= 0),
    fecha TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_item, id_ubicacion)
);

CREATE TABLE IF NOT EXISTS MOVIMIENTO (
    id_movimiento SERIAL PRIMARY KEY,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    fecha TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT NULL,
    id_tipo_mov INT NOT NULL REFERENCES TIPO_MOVIMIENTO(id_tipo_mov) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_item INT NOT NULL REFERENCES ITEM(id_item) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_usuario INT NOT NULL REFERENCES USUARIO(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ubicacion_origen INT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE SET NULL,
    id_ubicacion_destino INT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS INSPECCION (
    id_inspeccion SERIAL PRIMARY KEY,
    fecha TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_tipo_inspeccion INT NOT NULL REFERENCES TIPO_INSPECCION(id_tipo_inspeccion) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_usuario INT NOT NULL REFERENCES USUARIO(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ubicacion INT NOT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS DETALLE_INSPECCION (
    id_detalle SERIAL PRIMARY KEY,
    cantidad_encontrada INT NOT NULL CHECK (cantidad_encontrada >= 0),
    cantidad_teorica_actual INT NOT NULL CHECK (cantidad_teorica_actual >= 0),
    estado_reportado VARCHAR(50) NOT NULL DEFAULT 'OPERATIVO',
    id_inspeccion INT NOT NULL REFERENCES INSPECCION(id_inspeccion) ON UPDATE CASCADE ON DELETE CASCADE,
    id_item INT NOT NULL REFERENCES ITEM(id_item) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ALERTA_DISCREPANCIA (
    id_alerta SERIAL PRIMARY KEY,
    fecha_generacion TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resuelta BOOLEAN NOT NULL DEFAULT FALSE,
    diferencia INT NOT NULL,
    fecha_resolucion TIMESTAMP WITH TIME ZONE NULL,
    observaciones TEXT NULL,
    id_detalle INT NOT NULL UNIQUE REFERENCES DETALLE_INSPECCION(id_detalle) ON UPDATE CASCADE ON DELETE CASCADE,
    id_estado_alerta INT NOT NULL REFERENCES ESTADO_ALERTA(id_estado_alerta) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_usuario INT NULL REFERENCES USUARIO(id_usuario) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO ROL (nombre) VALUES 
('DIRECTOR'), ('CAPITAN'), ('TENIENTE'), ('ENCARGADO_INVENTARIO'), ('BOMBERO_VOLUNTARIO'), ('ADMIN_PORTAL')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO TIPO_ITEM (tipo_clasificacion) VALUES 
('AGRUPABLE_LOTE'), ('UNITARIO_ETIQUETABLE')
ON CONFLICT (tipo_clasificacion) DO NOTHING;

INSERT INTO CATEGORIA_ITEM (nombre) VALUES 
('Mobiliario y Cuartel'), ('Herramientas Menores'), ('Equipos de Proteccion Personal (EPP)'), 
('Insumos Medicos y Botiquin'), ('Cocina y Aseo'), ('Vehiculos y Material Mayor'), ('Tecnologia y Comunicaciones')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO TIPO_UBICACION (tipo) VALUES 
('CARRO_BOMBA'), ('BODEGA_CENTRAL'), ('CABANA_PANOL'), ('COMPARTIMENTO_CORTINA'), ('ESTANTE_BODEGA')
ON CONFLICT (tipo) DO NOTHING;

INSERT INTO TIPO_MOVIMIENTO (tipo_mov) VALUES 
('ALTA_COMPRA'), ('ALTA_DONACION'), ('TRASLADO'), ('DEVOLUCION'), 
('EXTRAVIO_EMERGENCIA'), ('BAJA_DETERIORO'), ('RECUPERACION_POST_SINIESTRO'), ('AJUSTE_INVENTARIO')
ON CONFLICT (tipo_mov) DO NOTHING;

INSERT INTO TIPO_INSPECCION (nombre, descripcion) VALUES 
('RUTINARIA_PERIODICA', 'Inspeccion y mantenimiento programado de inventario'),
('POST_EMERGENCIA', 'Recuento rapido de material tras retorno de acto de servicio')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO ESTADO_ALERTA (nombre, descripcion) VALUES 
('PENDIENTE', 'Discrepancia detectada en terreno, en espera de revision oficial'),
('RESUELTA_HALLAZGO', 'Material localizado internamente sin merma patrimonial'),
('CONFIRMADA_EXTRAVIO', 'Perdida definitiva ratificada tras siniestro multi-compania'),
('TRAMITADA_BAJA', 'Material danado e inutilizado derivado a proceso formal de baja'),
('DESCARTADA', 'Error de digitacion o falsa alarma durante el conteo')
ON CONFLICT (nombre) DO NOTHING;

-- Usuario inicial de pruebas
INSERT INTO USUARIO (id_usuario, nombre, email, id_rol) VALUES
(1, 'Cristian Jimenez', 'cristian.jimenez2201@alumnos.ubiobio.cl', 1),
(2, 'Matias Aguilera', 'matias.aguilera@alumnos.ubiobio.cl', 2)
ON CONFLICT (id_usuario) DO NOTHING;
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ejecutar DDL al iniciar para asegurar que la base de datos este inicializada
    try:
        with engine.connect() as conn:
            conn.execute(text(DDL_MER_V3))
            conn.commit()
            print("Base de datos MER v3 inicializada correctamente.")
    except Exception as e:
        print(f"Aviso inicializando BD: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "API REST de Staging para el Módulo de Inventarios "
        "(Proyecto de Título UBB - Cristian Jiménez & Matías Aguilera)"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS habilitado para desarrollo y pruebas móviles
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

        return {
            "status": "HEALTHY",
            "database": "CONNECTED",
            "engine": "PostgreSQL 16",
            "seed_data": {"roles_cargados": roles_count, "categorias_cargadas": categorias_count},
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error conectando a la base de datos: {e!s}",
        ) from e
