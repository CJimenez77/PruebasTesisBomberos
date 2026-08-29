import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ejecuta el script DDL del MER v3 y el dataset sintetico de Bomberos antes de los tests."""
    init_sql_path = os.path.join(os.path.dirname(__file__), "..", "..", "init-db.sql")
    if os.path.exists(init_sql_path):
        with open(init_sql_path, "r", encoding="utf-8") as f:
            ddl_content = f.read()
        with engine.connect() as conn:
            conn.execute(text(ddl_content))
            conn.commit()
    yield


@pytest.fixture
def client():
    """Fixture de cliente de pruebas para FastAPI con soporte de lifespan."""
    with TestClient(app) as c:
        yield c
