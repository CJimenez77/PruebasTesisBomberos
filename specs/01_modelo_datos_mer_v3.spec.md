# 🗄️ Especificación Formal del Modelo de Datos (MER v3 - 3FN)
## Proyecto de Titulación | Universidad del Bío-Bío (UBB)

> **Propósito para Gentle-AI / SDD:** Define la especificación técnica inmutable de las 15 tablas relacionales en PostgreSQL 16 para la generación de modelos SQLAlchemy y esquemas Pydantic.

---

## 📋 Catálogo de Tablas y Atributos

### 1. Tablas Maestras de Clasificación
* **`ROL` (`id_rol` PK, `nombre` UNIQUE):** `DIRECTOR`, `CAPITAN`, `TENIENTE`, `ENCARGADO_INVENTARIO`, `BOMBERO_VOLUNTARIO`, `ADMIN_PORTAL`.
* **`USUARIO` (`id_usuario` PK, `id_voluntario` NULL, `nombre`, `email` UNIQUE, `id_rol` FK a ROL).
* **`CATEGORIA_ITEM` (`id_categoria` PK, `nombre` UNIQUE):** Mobiliario, Herramientas Menores, EPP, Insumos Médicos, Cocina, Vehículos, Tecnología.
* **`TIPO_ITEM` (`id_tipo_item` PK, `tipo_clasificacion` UNIQUE):** `AGRUPABLE_LOTE` vs `UNITARIO_ETIQUETABLE`.
* **`TIPO_UBICACION` (`id_tipo_ubicacion` PK, `tipo` UNIQUE):** `CARRO_BOMBA`, `BODEGA_CENTRAL`, `CABANA_PANOL`, `COMPARTIMENTO_CORTINA`, `ESTANTE_BODEGA`.
* **`TIPO_MOVIMIENTO` (`id_tipo_mov` PK, `tipo_mov` UNIQUE):** `ALTA_COMPRA`, `ALTA_DONACION`, `TRASLADO`, `DEVOLUCION`, `EXTRAVIO_EMERGENCIA`, `BAJA_DETERIORO`, `RECUPERACION_POST_SINIESTRO`, `AJUSTE_INVENTARIO`.
* **`TIPO_INSPECCION` (`id_tipo_inspeccion` PK, `nombre` UNIQUE, `descripcion` TEXT):** `RUTINARIA_PERIODICA`, `POST_EMERGENCIA`.
* **`ESTADO_ALERTA` (`id_estado_alerta` PK, `nombre` UNIQUE, `descripcion` TEXT):** `PENDIENTE`, `RESUELTA_HALLAZGO`, `CONFIRMADA_EXTRAVIO`, `TRAMITADA_BAJA`, `DESCARTADA`.

---

### 2. Tablas Principales de Inventario y Distribución
* **`UBICACION`:**
  * `id_ubicacion` SERIAL PRIMARY KEY
  * `nombre` VARCHAR(100) NOT NULL
  * `descripcion` TEXT NULL
  * `id_tipo_ubicacion` INT NOT NULL REFERENCES `TIPO_UBICACION`
  * `id_ubicacion_padre` INT NULL REFERENCES `UBICACION` (Relación Reflexiva Cíclica)
* **`ITEM`:**
  * `id_item` SERIAL PRIMARY KEY
  * `codigo_qr` VARCHAR(100) NULL UNIQUE (Nullable para bienes agrupables)
  * `nombre` VARCHAR(150) NOT NULL
  * `descripcion` TEXT NULL
  * `estado` VARCHAR(50) NOT NULL DEFAULT 'OPERATIVO'
  * `cantidad` INT NOT NULL DEFAULT 1 CHECK (cantidad >= 0)
  * `fecha_vencimiento` DATE NULL (Caducidad perecibles o mantención extintores/vehículos)
  * `id_categoria` INT NOT NULL REFERENCES `CATEGORIA_ITEM`
  * `id_tipo_item` INT NOT NULL REFERENCES `TIPO_ITEM`
* **`ASIGNACION_ITEMS` (Saldo Actual Físico):**
  * `id_item` INT NOT NULL REFERENCES `ITEM`
  * `id_ubicacion` INT NOT NULL REFERENCES `UBICACION`
  * `cantidad_asignada` INT NOT NULL DEFAULT 1 CHECK (cantidad_asignada >= 0)
  * `fecha` TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
  * PRIMARY KEY (`id_item`, `id_ubicacion`)

---

### 3. Trazabilidad e Inspecciones
* **`MOVIMIENTO` (Ledger Inmutable Append-Only):**
  * `id_movimiento` SERIAL PRIMARY KEY
  * `cantidad` INT NOT NULL CHECK (cantidad > 0)
  * `fecha` TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
  * `observaciones` TEXT NULL
  * `id_tipo_mov` INT NOT NULL REFERENCES `TIPO_MOVIMIENTO`
  * `id_item` INT NOT NULL REFERENCES `ITEM`
  * `id_usuario` INT NOT NULL REFERENCES `USUARIO`
  * `id_ubicacion_origen` INT NULL REFERENCES `UBICACION` (NULL en compras/altas)
  * `id_ubicacion_destino` INT NULL REFERENCES `UBICACION` (NULL en bajas)
* **`INSPECCION`:**
  * `id_inspeccion` SERIAL PRIMARY KEY
  * `fecha` TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  * `id_tipo_inspeccion` INT NOT NULL REFERENCES `TIPO_INSPECCION`
  * `id_usuario` INT NOT NULL REFERENCES `USUARIO`
  * `id_ubicacion` INT NOT NULL REFERENCES `UBICACION`
* **`DETALLE_INSPECCION`:**
  * `id_detalle` SERIAL PRIMARY KEY
  * `cantidad_encontrada` INT NOT NULL CHECK (cantidad_encontrada >= 0)
  * `cantidad_teorica_actual` INT NOT NULL CHECK (cantidad_teorica_actual >= 0)
  * `estado_reportado` VARCHAR(50) DEFAULT 'OPERATIVO'
  * `id_inspeccion` INT NOT NULL REFERENCES `INSPECCION`
  * `id_item` INT NOT NULL REFERENCES `ITEM`
* **`ALERTA_DISCREPANCIA`:**
  * `id_alerta` SERIAL PRIMARY KEY
  * `fecha_generacion` TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  * `resuelta` BOOLEAN NOT NULL DEFAULT FALSE
  * `diferencia` INT NOT NULL (cantidad_encontrada - cantidad_teorica_actual)
  * `fecha_resolucion` TIMESTAMP WITH TIME ZONE NULL
  * `observaciones` TEXT NULL
  * `id_detalle` INT NOT NULL UNIQUE REFERENCES `DETALLE_INSPECCION`
  * `id_estado_alerta` INT NOT NULL REFERENCES `ESTADO_ALERTA`
  * `id_usuario` INT NULL REFERENCES `USUARIO` (Oficial que autoriza el cierre)
