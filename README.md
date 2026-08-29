# 🚒 Sistema de Gestión de Inventarios — Sexta Compañía de Bomberos
## Proyecto de Titulación | Universidad del Bío-Bío (UBB)
### Autores: Cristian Jiménez Fuentes & Matías Aguilera Ibarra

Servidor de Pruebas (Staging) desarrollado bajo metodología **Spec-Driven Development (SDD)** con el arnés **gentle-ai** y memoria persistente **engram**.

---

## 📁 Estructura del Proyecto

```
app-inventario-bomberos/
├── .gentle/                  # Configuración del arnés gentle-ai y memoria engram
│   └── config.json
├── specs/                    # Especificaciones formales (SDD)
│   └── 00_architecture_and_memory.spec.md
├── backend/                  # API REST en FastAPI (Python 3.12)
│   ├── app/
│   │   ├── core/             # Configuración, JWT, seguridad
│   │   ├── models/           # Modelos SQLAlchemy (MER v3)
│   │   ├── schemas/          # Esquemas Pydantic v2
│   │   ├── routers/          # Endpoints de API REST
│   │   ├── database.py       # Conexión a PostgreSQL (Render/Local)
│   │   └── main.py           # App principal FastAPI y Swagger (/docs)
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml        # Orquestador local con PostgreSQL 16 + FastAPI
├── init-db.sql               # Script DDL inicial con las 15 tablas del MER v3
├── render.yaml               # Blueprint para despliegue automático en Render Cloud
└── README.md
```

---

## 🚀 Cómo ejecutar en desarrollo local

```bash
cd app-inventario-bomberos
docker-compose up --build
```
* **API y Swagger:** `http://localhost:8000/docs`
* **Base de datos PostgreSQL:** `localhost:5432` (User: `postgres`, Password: `bomberos2026_staging_secret`, DB: `bomberos_inventario`)

---

## ☁️ Despliegue en Render (Staging Cloud)

1. En [Render.com](https://dashboard.render.com), haz clic en **`+ New`** $\rightarrow$ **`Blueprint`**.
2. Conecta el repositorio de GitHub y selecciona el archivo `render.yaml`.
3. Render levantará automáticamente la base de datos PostgreSQL 16 y el servicio web FastAPI con HTTPS.
