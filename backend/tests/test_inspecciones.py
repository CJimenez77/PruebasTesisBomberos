def test_get_tipos_inspeccion(client):
    """Valida los tipos de inspección del sistema"""
    response = client.get("/api/v1/inspecciones/tipos")
    assert response.status_code == 200
    tipos = response.json()
    assert len(tipos) == 2
    nombres = [t["nombre"] for t in tipos]
    assert "POST_EMERGENCIA" in nombres
    assert "RUTINARIA_PERIODICA" in nombres


def test_create_inspeccion_and_auto_generate_alert(client):
    """Valida que una inspección con discrepancia genere una ALERTA_DISCREPANCIA automática"""
    # 1. Login
    login_res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "capitan@bomberoschillanviejo.cl",
            "password": "any",
        },
    )
    token = login_res.json()["access_token"]

    # 2. Registrar inspección en Carro B-6 (1) con 1 manguera faltante
    payload = {
        "id_tipo_inspeccion": 2,  # POST_EMERGENCIA
        "id_ubicacion": 1,  # Carro B-6
        "detalles": [
            {
                "id_item": 1,  # Mangueras 70mm
                "cantidad_encontrada": 7,  # Se encontraron 7 pero debían haber 8
                "cantidad_teorica_actual": 8,
                "estado_reportado": "OPERATIVO",
            }
        ],
    }

    response = client.post(
        "/api/v1/inspecciones/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["tipo_nombre"] == "POST_EMERGENCIA"
    assert "Rodrigo Silva" in data["usuario_nombre"]


def test_list_and_resolve_alert(client):
    """Valida listado de alertas de discrepancia y resolución por parte del Director"""
    # 1. Login Director
    login_res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "director@bomberoschillanviejo.cl",
            "password": "any",
        },
    )
    token = login_res.json()["access_token"]

    # 2. Listar alertas
    res_alertas = client.get("/api/v1/inspecciones/alertas")
    assert res_alertas.status_code == 200
    alertas = res_alertas.json()
    assert len(alertas) >= 1

    id_alerta = alertas[0]["id_alerta"]

    # 3. Resolver alerta como RESUELTA_HALLAZGO (2)
    payload_resolve = {
        "id_estado_alerta": 2,  # RESUELTA_HALLAZGO
        "observaciones": "El material fue encontrado en el pañol de la Segunda Compañía y retornado al cuartel.",
    }

    res_resolve = client.post(
        f"/api/v1/inspecciones/alertas/{id_alerta}/resolver",
        json=payload_resolve,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res_resolve.status_code == 200
    alerta_resuelta = res_resolve.json()
    assert alerta_resuelta["resuelta"] is True
    assert alerta_resuelta["estado_nombre"] == "RESUELTA_HALLAZGO"
    assert "Carlos Mendoza" in alerta_resuelta["usuario_resolutor_nombre"]
