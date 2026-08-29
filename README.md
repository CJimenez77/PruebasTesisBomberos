# 🚒 Sistema de Gestión de Inventarios — Sexta Compañía de Bomberos
## Proyecto de Titulación | Universidad del Bío-Bío (UBB)
### Autores: Cristian Jiménez Fuentes & Matías Aguilera Ibarra

Servidor de Pruebas y Staging desarrollado bajo metodología **Spec-Driven Development (SDD)** con el arnés **gentle-ai** y memoria persistente **engram**.

---

## 📁 Estructura del Proyecto

```
app-inventario-bomberos/
├── .gentle/                  # Configuración del arnés gentle-ai y memoria engram
│   └── config.json
├── specs/                    # Especificaciones formales y contratos (SDD)
│   └── 00_architecture_and_memory.spec.md
├── backend/                  # API REST en FastAPI (Python 3.12)
│   ├── app/
│   │   ├── core/             # Configuración, JWT, seguridad
│   │   ├── models/           # Modelos SQLAlchemy (MER v3)
│   │   ├── schemas/          # Esquemas Pydantic v2
│   │   ├── routers/          # Endpoints de API REST
│   │   ├── database.py       # Conexión a PostgreSQL (Docker)
│   │   └── main.py           # App principal FastAPI y Swagger (/docs)
│   ├── tests/                # Pruebas unitarias con Pytest
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml        # Orquestador Docker con PostgreSQL 16 + FastAPI
├── init-db.sql               # Script DDL inicial con las 15 tablas del MER v3
└── README.md
```

---

## 🚀 Cómo ejecutar en Codespaces o Local

```bash
docker compose up -d --build
```
* **API REST y Swagger UI:** `http://localhost:8000/docs`
* **Base de datos PostgreSQL:** `localhost:5432` (User: `postgres`, Password: `bomberos2026_staging_secret`, DB: `bomberos_inventario`)
