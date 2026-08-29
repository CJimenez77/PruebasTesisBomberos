from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Valida el endpoint raiz y metadatos del proyecto"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["sistema"] == "Módulo de Gestión de Inventarios - Sexta Compañía de Bomberos"
    assert data["estado"] == "Operativo"
    assert "Cristian Jiménez" in data["autores"]

def test_health_check_endpoint():
    """Valida la conexion con la base de datos PostgreSQL y carga de datos semilla"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["database"] == "CONNECTED"
    assert data["engine"] == "PostgreSQL 16"
    assert data["seed_data"]["roles_cargados"] >= 6
    assert data["seed_data"]["categorias_cargadas"] >= 7

def test_listar_categorias():
    """Valida que el catalogo retorne las categorias institucionales oficiales"""
    response = client.get("/api/v1/inventario/categorias")
    assert response.status_code == 200
    categorias = response.json()
    assert isinstance(categorias, list)
    assert len(categorias) >= 7
    nombres = [c["nombre"] for c in categorias]
    assert "Herramientas Menores" in nombres
    assert "Equipos de Proteccion Personal (EPP)" in nombres
    assert "Vehiculos y Material Mayor" in nombres

def test_listar_tipos_movimiento():
    """Valida que los tipos de movimiento maestro de trazabilidad esten cargados"""
    response = client.get("/api/v1/inventario/tipos-movimiento")
    assert response.status_code == 200
    tipos = response.json()
    assert isinstance(tipos, list)
    assert len(tipos) >= 8
    tipos_mov = [t["tipo_mov"] for t in tipos]
    assert "ALTA_COMPRA" in tipos_mov
    assert "TRASLADO" in tipos_mov
    assert "EXTRAVIO_EMERGENCIA" in tipos_mov
    assert "RECUPERACION_POST_SINIESTRO" in tipos_mov
