def test_get_categorias(client):
    """Valida consulta de categorías del MER v3"""
    response = client.get("/api/v1/catalogo/categorias")
    assert response.status_code == 200
    categorias = response.json()
    assert len(categorias) >= 7
    nombres = [c["nombre"] for c in categorias]
    assert "Herramientas Menores" in nombres
    assert "Equipos de Proteccion Personal (EPP)" in nombres


def test_get_tipos_item(client):
    """Valida los 2 tipos de ítem: Agrupables vs Unitarios con QR"""
    response = client.get("/api/v1/catalogo/tipos-item")
    assert response.status_code == 200
    tipos = response.json()
    assert len(tipos) == 2
    nombres = [t["tipo_clasificacion"] for t in tipos]
    assert "AGRUPABLE_LOTE" in nombres
    assert "UNITARIO_ETIQUETABLE" in nombres


def test_create_item_agrupable(client):
    """Valida creación de ítem de recuento / agrupable (ej. Manguera 70mm)"""
    payload = {
        "nombre": "Manguera de Ataque 70mm Extra",
        "descripcion": "Manguera semirrígida color naranja para Carro B-6",
        "codigo_qr": None,
        "estado": "OPERATIVO",
        "cantidad": 12,
        "id_categoria": 2,  # Herramientas Menores
        "id_tipo_item": 1,  # AGRUPABLE_LOTE
    }
    response = client.post("/api/v1/catalogo/items", json=payload)
    assert response.status_code == 201
    item = response.json()
    assert item["nombre"] == payload["nombre"]
    assert item["cantidad"] == 12
    assert item["tipo_clasificacion"] == "AGRUPABLE_LOTE"


def test_create_item_unitario_qr(client):
    """Valida creación de bien individualizado con código QR"""
    payload = {
        "nombre": "Motosierra Stihl MS 362 Respaldo",
        "descripcion": "Herramienta de entrada forzada con etiqueta QR",
        "codigo_qr": "QR-TEST-NEW-099",
        "estado": "OPERATIVO",
        "cantidad": 1,
        "id_categoria": 2,  # Herramientas Menores
        "id_tipo_item": 2,  # UNITARIO_ETIQUETABLE
    }
    response = client.post("/api/v1/catalogo/items", json=payload)
    assert response.status_code == 201
    item = response.json()
    assert item["codigo_qr"] == "QR-TEST-NEW-099"
    assert item["tipo_clasificacion"] == "UNITARIO_ETIQUETABLE"


def test_create_duplicate_qr_fails(client):
    """Valida que no se permitan dos bienes con el mismo código QR (400 Bad Request)"""
    payload = {
        "nombre": "Otra Motosierra",
        "descripcion": "Intento de duplicar QR",
        "codigo_qr": "QR-MOTO-001",  # Ya existe en el dataset sintético
        "estado": "OPERATIVO",
        "cantidad": 1,
        "id_categoria": 2,
        "id_tipo_item": 2,
    }
    response = client.post("/api/v1/catalogo/items", json=payload)
    assert response.status_code == 400
    assert "QR-MOTO-001" in response.json()["detail"]


def test_filter_items_by_qr(client):
    """Valida búsqueda instantánea por código QR"""
    response = client.get("/api/v1/catalogo/items?codigo_qr=QR-MOTO-001")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert "Motosierra Stihl" in items[0]["nombre"]
