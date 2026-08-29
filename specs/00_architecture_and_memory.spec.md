# Contexto y Memoria de Dominio: Módulo de Gestión de Inventarios
## Proyecto de Título - Universidad del Bío-Bío (UBB)
### Beneficiario: Sexta Compañía de Bomberos de Chillán Viejo

Este documento define la memoria contextual permanente (`engram`) y los principios arquitectónicos no negociables (*guardrails*) que todo agente de desarrollo debe respetar:

---

## 1. Reglas de Dominio Bomberil (Inmutables)

1. **Bifurcación de Ítems (`TIPO_ITEM`):**
   * **Bienes Etiquetables / Unitarios:** Se individualizan con código QR (`ITEM.codigo_qr`), cantidad total = 1. Mobiliario, computadores, generadores.
   * **Bienes de Recuento / Agrupables:** Herramientas expuestas a fuego/agua (mangueras, hachas, pitones). No llevan QR individual; se identifican institucionalmente por color naranja y se cuentan por lotes.
2. **Diferenciación entre Estado Actual (`ASIGNACION_ITEMS`) y Eventos (`MOVIMIENTO`):**
   * `ASIGNACION_ITEMS` representa el **saldo actual** en cada ubicación física. **NO** lleva `id_usuario`.
   * `MOVIMIENTO` es el **ledger inmutable (solo inserción / append-only)**. Nunca se hace UPDATE ni DELETE sobre esta tabla. Registra quién (`id_usuario`), cuándo (`fecha`), qué (`id_item`, `cantidad`), y de dónde a dónde (`id_ubicacion_origen` $\rightarrow$ `id_ubicacion_destino`).
3. **Semántica de Altas y Bajas:**
   * **Alta (Compra / Donación):** `id_ubicacion_origen = NULL`, `id_ubicacion_destino = Ubicación`.
   * **Baja (Deterioro / Extravío):** `id_ubicacion_origen = Ubicación`, `id_ubicacion_destino = NULL`. Requiere autorización de jefatura (RF-12).
   * **Reaparición post-siniestro:** Se inserta un nuevo movimiento de tipo `RECUPERACION_POST_SINIESTRO` (`origen = NULL`, `destino = Carro`).
4. **Ubicaciones Jerárquicas Cíclicas (`UBICACION`):**
   * Relación reflexiva con `id_ubicacion_padre` (Nullable). Permite modelar:
     * Carro B-6 (Raíz) $\rightarrow$ Cortina Izquierda 1 (Hijo) $\rightarrow$ Bandeja Superior (Nieto).
5. **Vigencias y Vencimientos (`fecha_vencimiento`):**
   * En `ITEM`, campo de fecha multiuso para caducidad de perecibles (alimentos, botiquín) y próxima mantención/revisión técnica de extintores y vehículos.

---

## 2. Contratos Tecnológicos y Estándares de Código

* **Backend:** FastAPI + Python 3.12 + SQLAlchemy 2.0 (declarative mapping) + Pydantic v2.
* **Base de Datos:** PostgreSQL 16 normalizado estrictamente en 3FN (15 tablas).
* **Validación de Tipos:** Tipado estricto en todos los routers, services y schemas.
* **Testing Obligatorio:** Toda historia de usuario o endpoint debe incluir su respectivo archivo de pruebas unitarias en `backend/tests/` con Pytest.
