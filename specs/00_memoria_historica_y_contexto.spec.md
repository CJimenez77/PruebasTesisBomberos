# 🧠 Memoria Histórica, Contexto Institucional y Decisiones de Arquitectura
## Proyecto de Titulación | Universidad del Bío-Bío (UBB)
### Autores: Cristian Jiménez Fuentes & Matías Aguilera Ibarra
### Beneficiario: Sexta Compañía de Bomberos de Chillán Viejo

> **Propósito para Engram:** Este documento contiene la memoria contextual completa y permanente de todo el proyecto, sus decisiones técnicas fundamentales y la justificación histórica de cada componente para el agente `gentle-ai`.

---

## 🏛️ 1. Contexto Académico e Institucional

* **Institución:** Universidad del Bío-Bío (UBB), Facultad de Ciencias Empresariales / Departamento de Ciencias de la Computación y Tecnologías de la Información.
* **Carrera:** Ingeniería Civil en Informática.
* **Proyecto:** Plataforma de Gestión Institucional para la Sexta Compañía de Bomberos de Chillán Viejo.
* **Módulo Asignado:** Módulo de Gestión de Inventarios, Trazabilidad de Activos y Auditoría Post-Emergencia.
* **Arquitectura Global:** Ecosistema modular de 3 microservicios concurrentes (Personal, Tesorería, Inventarios) coordinados por un Portal Principal con autenticación centralizada (JWT / RBAC) y base de datos PostgreSQL compartida.
* **Hito Crítico Fatal:** **Viernes 27 de noviembre de 2026 (12:00 hrs)** — Primera fecha de entrega de informe a profesor informante (para evitar arancel del semestre 2027-1).

---

## 🗺️ 2. Evolución Histórica y Justificaciones del MER (de v1 a v3 Oficial)

A lo largo del proyecto, el modelo de datos evolucionó para resolver problemas reales de la operación bomberil:

### A. Jerarquía de Ubicaciones Cíclica (Eliminación de `SUB_UBICACION`)
* **Problema en v1:** `SUB_UBICACION` creaba doble clave foránea y limitaba la jerarquía a solo 2 niveles fijos.
* **Solución v3:** Relación reflexiva cíclica en `UBICACION` (`id_ubicacion_padre` Nullable). Modela infinitos niveles: Cuartel $\rightarrow$ Carro B-6 $\rightarrow$ Cortina 1 $\rightarrow$ Gaveta Superior.

### B. Doble Relación Explícita ORIGEN y DESTINO en `MOVIMIENTO`
* **Problema:** Trasladar material entre carros bomba o desde bodega a carros requería saber origen y destino exactos, soportando compras y bajas.
* **Solución v3:** Dos relaciones $1:N$ independientes (rombos `ORIGEN` y `DESTINO`) en Chen y dos FKs en PostgreSQL: `id_ubicacion_origen` (NULL en compras) y `id_ubicacion_destino` (NULL en bajas).

### C. Diferencia Conceptual entre `ASIGNACION_ITEMS` y `MOVIMIENTO`
* **`ASIGNACION_ITEMS`:** Representa el **saldo actual** en cada ubicación. **NO** tiene relación con `USUARIO`, porque no es una acción humana sino el estado físico actual del inventario.
* **`MOVIMIENTO`:** Es el **ledger inmutable (append-only)** que audita la acción humana. Contiene `id_usuario`, `fecha`, `cantidad`, `id_tipo_mov`, `origen` y `destino`. Nunca se borra ni se modifica.

### D. Clasificación Dual de Bienes (`TIPO_ITEM`)
* **Bienes Unitarios / Etiquetables:** Mobiliario, generadores, computadores. Llevan código QR único (`codigo_qr`), cantidad total = 1.
* **Bienes Agrupables / Lote:** Herramientas de agua/fuego (mangueras, hachas, pitones). No llevan QR individual (se deteriora con el fuego/hollín), se identifican por color institucional naranja y se gestionan por recuento numérico.

### E. Soporte para Reaparición de Material Perdido
* Cuando una herramienta perdida en un siniestro reaparece devuelta por otra compañía, no se altera el historial del incendio. Se registra un nuevo `MOVIMIENTO` de tipo `RECUPERACION_POST_SINIESTRO` (`Origen: NULL` $\rightarrow$ `Destino: Carro/Bodega`), reincorporando automáticamente las unidades al saldo.

---

## 🛡️ 3. Justificación de Ingeniería del Stack Tecnológico (FastAPI vs Spring Boot)

1. **Concurrencia Asíncrona (ASGI vs Servlets):** FastAPI corre sobre Starlette y uvloop con rendimiento comparable a C++/Go para operaciones I/O-bound intensivas de base de datos.
2. **Contratos OpenAPI 3.1 Nativos:** En FastAPI, OpenAPI y JSON Schema se generan automáticamente desde los tipos de Pydantic, garantizando integración sin fricción con los módulos de Personal y Tesorería.
3. **Tipado Estricto y Validación:** Pydantic v2 (núcleo en Rust) rechaza payloads corruptos con código 422 antes de procesar lógica de negocio.
4. **Huella de Memoria RAM (Restricción Real de Bomberos):** FastAPI consume 60-120 MB por contenedor vs 600 MB - 1.5 GB de Spring Boot (JVM), permitiendo correr todo el stack en servidores de bajo costo.
5. **Velocidad de Desarrollo:** Reducción del 60% de código boilerplate, mitigando el riesgo de atrasos para la fecha de titulación.

---

## 📅 4. Planificación de Sprints (Jira Scrum — Key: INVENTARIO)

* **Sprint 0 — Setup & Diseño (25 Ago - 11 Sep):** Entorno, Docker, MER v3, Base de datos, Auth JWT base.
* **Sprint 1 — Portal & Catálogo (14 Sep - 02 Oct):** CRUD Items, Agrupables vs Etiquetables, Carga QR, Ubicaciones jerárquicas.
* **Sprint 2 — Terreno & Alertas (05 Oct - 23 Oct):** Módulo de inspección móvil post-emergencia, detección de discrepancias, Ledger de movimientos.
* **Sprint 3 — Dashboard & Cierre (26 Oct - 13 Nov):** Reportes del Director, Exportación Excel/PDF, Pruebas de integración, Puesta en marcha.
