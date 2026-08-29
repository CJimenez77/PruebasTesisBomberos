# 📋 Estado Actual del Módulo de Inventarios: Staging, Frontend y Testing
## Proyecto de Titulación | Universidad del Bío-Bío (UBB)
### Autores: Cristian Jiménez Fuentes & Matías Aguilera Ibarra
### Beneficiario: Sexta Compañía de Bomberos de Chillán Viejo

> **Memoria Permanente en Engram / Specs:** Este documento registra el estado operacional actual del sistema, la arquitectura del frontend en Vue 3, la suite de pruebas automatizadas y las directivas institucionales aplicadas.

---

## 🏛️ 1. Identidad Visual y Experiencia Institucional
* **Cero Emojis:** Se eliminaron todos los emojis de la interfaz, el backend y el pipeline, reemplazándolos por **iconografía vectorial SVG profesional** y tipografía técnica sobria acorde a un servicio de emergencia.
* **Paleta de Colores Institucional (Dark Mode):**
  * Fondo Principal: `#211E1A` (Carbón)
  * Superficies y Tarjetas: `#2B2824` / `#33302B`
  * Granate Institucional: `#B81313`
  * Rojo Operativo: `#E71506`
  * Bordes y Separadores: `#4A453E`
* **Estándar de Estado:** Badges sobrios (`OPERATIVO`, `EN_MANTENCION`, `CONFORME`, `CRÍTICA PENDIENTE`).

---

## 👥 2. Accesos por Funcionalidades Operativas e Identidades Ficticias
El inicio de sesión (`/login`) cuenta con campos limpios por defecto y selector rápido por tareas del cuartel con identidades ficticias:

| Rol Institucional | Nombre Ficticio | Correo Institucional Ficticio | Contraseña Staging | Funcionalidad Operativa Principal |
| :--- | :--- | :--- | :--- | :--- |
| **Director** | Carlos Mendoza Rivas | `director@bomberoschillanviejo.cl` | `bomberos_secret_staging_2026` | Mando, auditoría y resolución/cierre de alertas |
| **Capitán** | Rodrigo Silva Morales | `capitan@bomberoschillanviejo.cl` | `bomberos_secret_staging_2026` | Inspecciones post-emergencia y recuento en terreno |
| **Teniente Primero** | Andrés Soto Valenzuela | `teniente1@bomberoschillanviejo.cl` | `bomberos_secret_staging_2026` | Altas por compra/donación y bajas por deterioro |
| **Encargado Inventario** | Patricio Fuentes Bravo | `inventario@bomberoschillanviejo.cl` | `bomberos_secret_staging_2026` | Traslados de stock y trazabilidad en el ledger |
| **Bombero Voluntario** | Felipe González Araya | `voluntario1@bomberoschillanviejo.cl` | `bomberos_secret_staging_2026` | Consulta de herramientas y guardia nocturna |

---

## 🏗️ 3. Arquitectura Frontend (Vue 3 + Vite + Tailwind + Pinia)

1. **Vistas Implementadas (`frontend/src/views/`):**
   * `DashboardView.vue`: Resumen ejecutivo del mando, métricas del cuartel y banner de alertas críticas activas.
   * `CatalogoView.vue`: Catálogo con búsqueda en tiempo real, filtro dual (con QR vs agrupables por lote) y modal de creación de ítems.
   * `CarrosView.vue`: Vista jerárquica de unidades vehiculares (Carro B-6, Unidad R-6, Bodega Central) y desglose de stock por cortinas/gavetas.
   * `InspeccionView.vue`: Checklist interactivo para recuento rápido con controles `+` / `−` y auto-generación de alertas por discrepancia.
   * `AlertasView.vue`: Tablero de discrepancias pendientes vs resueltas, modal de visación del Director y despacho de notificaciones.
   * `MovimientosView.vue`: Bitácora auditada del ledger inmutable append-only y formulario modal de traslados con validación atómica de saldo.
   * `LoginView.vue`: Autenticación con selector de perfiles funcionales.

2. **Gestión de Estado Centralizada (Pinia Stores en `frontend/src/stores/`):**
   * `auth.js`: Manejo de JWT, persistencia de sesión en `localStorage` y control RBAC.
   * `catalogo.js`: Catálogo de ítems, categorías y tipos de bien.
   * `ubicaciones.js`: Jerarquía de carros y bodegas.
   * `movimientos.js`: Ledger inmutable y tipos de movimiento.
   * `inspecciones.js`: Inspecciones, detalles y resolución de discrepancias.

---

## 🧪 4. Calidad y Pruebas Automatizadas (25 Tests Pytest)
* **Suite de Pruebas (`backend/tests/`):**
  * `test_api.py`: Endpoints raíz, health checks y catálogos base.
  * `test_auth.py`: Autenticación JWT, verificación de perfiles (`/auth/me`), roles y seguridad RBAC.
  * `test_catalogo.py`: Creación de bienes agrupables, unitarios con QR, validación de unicidad de QR y filtros.
  * `test_ubicaciones.py`: Creación de carros y compartimentos jerárquicos (relación reflexiva).
  * `test_movimientos.py`: Tipos de movimiento, historial y transacciones atómicas con validación de stock insuficiente.
  * `test_inspecciones.py`: Inspecciones operativas, detección automática de discrepancias y resolución formal por el Director.
* **Integración Continua (CI):**
  * Pipeline en GitHub Actions configurado con PostgreSQL 16 de pruebas, Ruff linter y Pytest con reporte de cobertura.
