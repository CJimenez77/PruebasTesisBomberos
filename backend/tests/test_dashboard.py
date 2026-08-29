def test_get_dashboard_summary(client):
    """Valida métricas consolidadas del Dashboard"""
    response = client.get("/api/v1/dashboard/resumen")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "total_unidades_stock" in data
    assert "total_carros" in data
    assert "alertas_pendientes" in data
    assert "ultimas_alertas" in data
    assert data["total_items"] >= 20
    assert data["total_carros"] >= 2
