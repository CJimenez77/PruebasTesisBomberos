import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Gestión de Inventarios - Bomberos 6ta Compañía"
    API_V1_STR: str = "/api/v1"

    # Seguridad JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bomberos_super_secret_jwt_key_2026_production_grade_security")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días para desarrollo/terreno

    # Base de Datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:bomberos2026_staging_secret@localhost:5432/bomberos_inventario",
    )

    class Config:
        case_sensitive = True


settings = Settings()
