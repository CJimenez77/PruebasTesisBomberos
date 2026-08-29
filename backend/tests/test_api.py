def test_root_endpoint(client):
    """Valida el endpoint raiz y metadatos del proyecto"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["sistema"] == "Módulo de Gestión de Inventarios - Sexta Compañía de Bomberos"
    assert data["estado"] == "Operativo"
    assert "Cristian Jiménez" in data["autores"]


def test_health_check_endpoint(client):
    """Valida la conexion con la base de datos PostgreSQL y carga de datos semilla"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["database"] == "CONNECTED"
    assert data["engine"] == "PostgreSQL 16"
    assert data["seed_data"]["roles_cargados"] >= 6
    assert data["seed_data"]["categorias_cargadas"] >= 7


def test_listar_categorias(client):
    """Valida que el catalogo retorne las categorias institucionales oficiales"""
    response = client.get("/api/v1/catalogo/categorias")
    assert response.status_code == 200
    categorias = response.json()
    assert isinstance(categorias, list)
    assert len(categorias) >= 7
    nombres = [c["nombre"] for c in categorias]
    assert "Herramientas Menores" in nombres
    assert "Equipos de Proteccion Personal (EPP)" in nombres
    assert "Vehiculos y Material Mayor" in nombres


def test_listar_tipos_ubicacion(client):
    """Valida que los tipos de ubicacion maestros esten cargados"""
    response = client.get("/api/v1/ubicaciones/tipos")
    assert response.status_code == 200
    tipos = response.json()
    assert isinstance(tipos, list)
    assert len(tipos) >= 5
    tipos_nombres = [t["tipo"] for t in tipos]
    assert "CARRO_BOMBA" in tipos_nombres
    assert "BODEGA_CENTRAL" in tipos_nombres
