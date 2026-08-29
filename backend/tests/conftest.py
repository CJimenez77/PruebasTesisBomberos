import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import engine
from app.main import DDL_MER_V3, app


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ejecuta el script DDL del MER v3 y datos semilla antes de los tests."""
    with engine.connect() as conn:
        conn.execute(text(DDL_MER_V3))
        conn.commit()
    yield


@pytest.fixture
def client():
    """Fixture de cliente de pruebas para FastAPI con soporte de lifespan."""
    with TestClient(app) as c:
        yield c
