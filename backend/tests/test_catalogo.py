def test_get_categorias(client):
    """Valida consulta de categorías maestras"""
    response = client.get("/api/v1/catalogo/categorias")
    assert response.status_code == 200
    categorias = response.json()
    assert len(categorias) >= 7


def test_get_tipos_item(client):
    """Valida los tipos de clasificación (Agrupable vs QR)"""
    response = client.get("/api/v1/catalogo/tipos-item")
    assert response.status_code == 200
    tipos = response.json()
    assert len(tipos) == 2
    clasificaciones = [t["tipo_clasificacion"] for t in tipos]
    assert "AGRUPABLE_LOTE" in clasificaciones
    assert "UNITARIO_ETIQUETABLE" in clasificaciones


def test_create_item_agrupable(client):
    """Valida creación de ítem de recuento / agrupable (ej. Manguera 70mm)"""
    payload = {
        "nombre": "Manguera de Ataque 70mm",
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
    assert item["nombre"] == "Manguera de Ataque 70mm"
    assert item["cantidad"] == 12
    assert item["codigo_qr"] is None
    assert item["tipo_clasificacion"] == "AGRUPABLE_LOTE"


def test_create_item_unitario_qr(client):
    """Valida creación de bien individualizado con código QR"""
    payload = {
        "nombre": "Motosierra Stihl MS 362",
        "descripcion": "Herramienta de entrada forzada con etiqueta QR",
        "codigo_qr": "QR-MOTO-001",
        "estado": "OPERATIVO",
        "cantidad": 1,
        "id_categoria": 2,  # Herramientas Menores
        "id_tipo_item": 2,  # UNITARIO_ETIQUETABLE
    }
    response = client.post("/api/v1/catalogo/items", json=payload)
    assert response.status_code == 201
    item = response.json()
    assert item["codigo_qr"] == "QR-MOTO-001"
    assert item["tipo_clasificacion"] == "UNITARIO_ETIQUETABLE"


def test_create_duplicate_qr_fails(client):
    """Valida que no se permitan códigos QR duplicados (error 400)"""
    payload = {
        "nombre": "Generador Honda 5kVA",
        "codigo_qr": "QR-MOTO-001",  # Ya usado en el test anterior
        "estado": "OPERATIVO",
        "cantidad": 1,
        "id_categoria": 2,
        "id_tipo_item": 2,
    }
    response = client.post("/api/v1/catalogo/items", json=payload)
    assert response.status_code == 400
    assert "Ya existe un ítem registrado con el código QR" in response.json()["detail"]


def test_filter_items_by_qr(client):
    """Valida búsqueda instantánea por código QR"""
    response = client.get("/api/v1/catalogo/items?codigo_qr=QR-MOTO-001")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["nombre"] == "Motosierra Stihl MS 362"
