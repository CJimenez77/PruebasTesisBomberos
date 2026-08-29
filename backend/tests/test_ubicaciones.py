def test_get_tipos_ubicacion(client):
    """Valida consulta de tipos de ubicación del MER v3"""
    response = client.get("/api/v1/ubicaciones/tipos")
    assert response.status_code == 200
    tipos = response.json()
    assert len(tipos) >= 5
    nombres = [t["tipo"] for t in tipos]
    assert "CARRO_BOMBA" in nombres
    assert "BODEGA_CENTRAL" in nombres
    assert "COMPARTIMENTO_CORTINA" in nombres


def test_create_carro_bomba_ubicacion(client):
    """Valida creación de un Carro Bomba (Ubicación Raíz)"""
    payload = {
        "nombre": "Carro Forestal B-7",
        "descripcion": "Unidad de ataque forestal 4x4",
        "id_tipo_ubicacion": 1,  # CARRO_BOMBA
        "id_ubicacion_padre": None,
    }
    response = client.post("/api/v1/ubicaciones/", json=payload)
    assert response.status_code == 201
    ub = response.json()
    assert ub["nombre"] == "Carro Forestal B-7"
    assert ub["id_ubicacion_padre"] is None
    assert ub["tipo_ubicacion_nombre"] == "CARRO_BOMBA"


def test_create_compartimento_jerarquico(client):
    """Valida creación de un compartimento dentro de un carro (Relación Reflexiva)"""
    # 1. Crear Carro
    carro_res = client.post(
        "/api/v1/ubicaciones/",
        json={
            "nombre": "Carro Portaescalas Q-6",
            "descripcion": "Unidad de zapadores y escalas",
            "id_tipo_ubicacion": 1,
            "id_ubicacion_padre": None,
        },
    )
    assert carro_res.status_code == 201
    carro_id = carro_res.json()["id_ubicacion"]

    # 2. Crear Compartimento hijo
    comp_res = client.post(
        "/api/v1/ubicaciones/",
        json={
            "nombre": "Bandeja Superior Escalas",
            "descripcion": "Escalas de triple extensión",
            "id_tipo_ubicacion": 4,  # COMPARTIMENTO_CORTINA
            "id_ubicacion_padre": carro_id,
        },
    )
    assert comp_res.status_code == 201
    comp = comp_res.json()
    assert comp["id_ubicacion_padre"] == carro_id
    assert comp["nombre"] == "Bandeja Superior Escalas"
