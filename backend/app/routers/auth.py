from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user
from app.database import get_db
from app.schemas.auth import RolResponse, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticación & Usuarios"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Inicio de sesión institucional para Bomberos.
    Retorna el Token JWT firmado con el rol del usuario para RBAC.
    """
    # En esta etapa inicial de staging, validamos por email y rol asignado
    user_row = db.execute(
        text("""
            SELECT u.id_usuario, u.nombre, u.email, u.id_rol, r.nombre as role_name
            FROM USUARIO u
            JOIN ROL r ON u.id_rol = r.id_rol
            WHERE u.email = :email
        """),
        {"email": form_data.username},
    ).fetchone()

    if not user_row:
        # Para desarrollo, si el usuario no existe, creamos un bombero por defecto si es @bomberos.cl o @alumnos.ubiobio.cl
        if "@" in form_data.username:
            db.execute(
                text("""
                    INSERT INTO USUARIO (nombre, email, id_rol) 
                    VALUES (:nombre, :email, 5)
                    ON CONFLICT (email) DO NOTHING
                """),
                {"nombre": form_data.username.split("@")[0].capitalize(), "email": form_data.username},
            )
            db.commit()
            user_row = db.execute(
                text("""
                    SELECT u.id_usuario, u.nombre, u.email, u.id_rol, r.nombre as role_name
                    FROM USUARIO u
                    JOIN ROL r ON u.id_rol = r.id_rol
                    WHERE u.email = :email
                """),
                {"email": form_data.username},
            ).fetchone()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o usuario no registrado.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    token = create_access_token(
        subject=user_row[2],  # email
        role=user_row[4],  # role_name (DIRECTOR, CAPITAN, etc.)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user_row[4],
        "user_id": user_row[0],
        "user_name": user_row[1],
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
):
    """Retorna el perfil del usuario autenticado actualmente."""
    return current_user


@router.get("/roles", response_model=List[RolResponse])
def get_roles(db: Session = Depends(get_db)):
    """Retorna el listado de roles institucionales del sistema."""
    result = db.execute(text("SELECT id_rol, nombre FROM ROL ORDER BY id_rol")).fetchall()
    return [{"id_rol": r[0], "nombre": r[1]} for r in result]
