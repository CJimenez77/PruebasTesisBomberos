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
    assert "Cristian Jiménez" in data["user_name"]


def test_auth_me_protected_endpoint(client):
    """Valida lectura de perfil de usuario autenticado mediante /auth/me"""
    # 1. Obtener Token
    login_res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "matias.aguilera@alumnos.ubiobio.cl",
            "password": "secret_staging",
        },
    )
    token = login_res.json()["access_token"]

    # 2. Consultar /me con Bearer token
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "matias.aguilera@alumnos.ubiobio.cl"
    assert "Matías Aguilera" in user_data["nombre"]
    assert user_data["role_name"] == "CAPITAN"


def test_auth_me_unauthorized_without_token(client):
    """Valida que acceder a rutas protegidas sin token retorne 401 Unauthorized"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_roles_list(client):
    """Valida listado de roles maestros del MER v3"""
    response = client.get("/api/v1/auth/roles")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) >= 6
    role_names = [r["nombre"] for r in roles]
    assert "DIRECTOR" in role_names
    assert "CAPITAN" in role_names
    assert "BOMBERO_VOLUNTARIO" in role_names
