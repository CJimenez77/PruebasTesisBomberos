def test_get_tipos_ubicacion(client):
    """Valida consulta de tipos maestros de ubicación"""
    response = client.get("/api/v1/ubicaciones/tipos")
    assert response.status_code == 200
    tipos = response.json()
    assert len(tipos) >= 5
    nombres_tipos = [t["tipo"] for t in tipos]
    assert "CARRO_BOMBA" in nombres_tipos
    assert "BODEGA_CENTRAL" in nombres_tipos
    assert "COMPARTIMENTO_CORTINA" in nombres_tipos


def test_create_carro_bomba_ubicacion(client):
    """Valida creación de un Carro Bomba (Ubicación Raíz)"""
    payload = {
        "nombre": "Carro Bomba B-6",
        "descripcion": "Unidad de primera intervención y rescate",
        "id_tipo_ubicacion": 1,  # CARRO_BOMBA
        "id_ubicacion_padre": None,
    }
    response = client.post("/api/v1/ubicaciones/", json=payload)
    assert response.status_code == 201
    carro = response.json()
    assert carro["nombre"] == "Carro Bomba B-6"
    assert carro["id_ubicacion_padre"] is None
    assert carro["tipo_nombre"] == "CARRO_BOMBA"


def test_create_compartimento_jerarquico(client):
    """Valida creación de un compartimento dentro de un carro (Relación Reflexiva)"""
    # 1. Crear Carro
    carro_res = client.post(
        "/api/v1/ubicaciones/",
        json={
            "nombre": "Carro R-6",
            "descripcion": "Unidad de rescate",
            "id_tipo_ubicacion": 1,
            "id_ubicacion_padre": None,
        },
    )
    id_carro = carro_res.json()["id_ubicacion"]

    # 2. Crear Cortina hija
    cortina_res = client.post(
        "/api/v1/ubicaciones/",
        json={
            "nombre": "Cortina Izquierda 1 (R-6)",
            "descripcion": "Gaveta de herramientas de corte",
            "id_tipo_ubicacion": 4,  # COMPARTIMENTO_CORTINA
            "id_ubicacion_padre": id_carro,
        },
    )
    assert cortina_res.status_code == 201
    cortina = cortina_res.json()
    assert cortina["nombre"] == "Cortina Izquierda 1 (R-6)"
    assert cortina["id_ubicacion_padre"] == id_carro
