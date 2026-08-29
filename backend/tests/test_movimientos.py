def test_get_tipos_movimiento(client):
    """Valida que los 8 tipos de movimiento maestros existan"""
    response = client.get("/api/v1/movimientos/tipos")
    assert response.status_code == 200
    tipos = response.json()
    assert len(tipos) >= 8
    nombres = [t["tipo_mov"] for t in tipos]
    assert "ALTA_COMPRA" in nombres
    assert "TRASLADO" in nombres
    assert "EXTRAVIO_EMERGENCIA" in nombres
    assert "RECUPERACION_POST_SINIESTRO" in nombres


def test_list_movimientos_history(client):
    """Valida consulta del ledger inmutable de movimientos"""
    response = client.get("/api/v1/movimientos/")
    assert response.status_code == 200
    movs = response.json()
    assert isinstance(movs, list)
    assert len(movs) >= 1


def test_create_traslado_movimiento(client):
    """Valida traslado de stock y registro en el ledger inmutable"""
    # 1. Login
    login_res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "director@bomberoschillanviejo.cl",
            "password": "any",
        },
    )
    token = login_res.json()["access_token"]

    # 2. Trasladar 2 mangueras (item 1) de Bodega Pañol (12) a Carro B-6 Cortina Izq 1 (5)
    payload = {
        "id_item": 1,
        "id_tipo_mov": 3,  # TRASLADO
        "cantidad": 2,
        "id_ubicacion_origen": 12,  # Bodega Pañol (tiene 8)
        "id_ubicacion_destino": 5,  # Carro B-6 Cortina Izq 1
        "observaciones": "Refuerzo de material para guardia nocturna",
    }

    response = client.post(
        "/api/v1/movimientos/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    mov = response.json()
    assert mov["cantidad"] == 2
    assert mov["id_tipo_mov"] == 3
    assert mov["id_ubicacion_origen"] == 12
    assert mov["id_ubicacion_destino"] == 5
    assert "Carlos Mendoza" in mov["usuario_nombre"]


def test_traslado_insufficient_stock_fails(client):
    """Valida que un traslado con stock insuficiente sea rechazado con 400"""
    login_res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "director@bomberoschillanviejo.cl",
            "password": "any",
        },
    )
    token = login_res.json()["access_token"]

    payload = {
        "id_item": 1,
        "id_tipo_mov": 3,
        "cantidad": 999,  # No existen 999 mangueras en esa ubicación
        "id_ubicacion_origen": 12,
        "id_ubicacion_destino": 5,
        "observaciones": "Intento inválido",
    }

    response = client.post(
        "/api/v1/movimientos/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["detail"]
