def test_login_success(client):
    """Valida inicio de sesión exitoso y entrega de Token JWT firmado"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "cristian.jimenez2201@alumnos.ubiobio.cl",
            "password": "any_password_for_staging",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["role"] == "DIRECTOR"
    assert data["user_name"] == "Cristian Jimenez"


def test_auth_me_protected_endpoint(client):
    """Valida acceso al perfil mediante Bearer Token JWT"""
    # 1. Login
    login_res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "cristian.jimenez2201@alumnos.ubiobio.cl",
            "password": "any_password",
        },
    )
    token = login_res.json()["access_token"]

    # 2. Acceder a /me
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "cristian.jimenez2201@alumnos.ubiobio.cl"
    assert user_data["role_name"] == "DIRECTOR"


def test_auth_me_unauthorized_without_token(client):
    """Valida rechazo 401 si no se envía Bearer token"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_roles_list(client):
    """Valida consulta de roles institucionales"""
    response = client.get("/api/v1/auth/roles")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) >= 6
    role_names = [r["nombre"] for r in roles]
    assert "DIRECTOR" in role_names
    assert "CAPITAN" in role_names
    assert "BOMBERO_VOLUNTARIO" in role_names
