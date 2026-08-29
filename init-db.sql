-- ==============================================================================
-- BASE DE DATOS OFICIAL Y DATASET SINTÉTICO DE ALTA FIDELIDAD
-- MÓDULO DE INVENTARIOS Y TRAZABILIDAD - SEXTA COMPAÑÍA DE BOMBEROS CHILLÁN VIEJO
-- TESIS UBB: CRISTIAN JIMÉNEZ FUENTES & MATÍAS AGUILERA IBARRA
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. TABLAS MAESTRAS DE CLASIFICACIÓN
CREATE TABLE IF NOT EXISTS ROL (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    id_voluntario INT NULL,
    nombre VARCHAR(100) NULL,
    email VARCHAR(100) NULL UNIQUE,
    id_rol INT NOT NULL REFERENCES ROL(id_rol) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS CATEGORIA_ITEM (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_ITEM (
    id_tipo_item SERIAL PRIMARY KEY,
    tipo_clasificacion VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_UBICACION (
    id_tipo_ubicacion SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_MOVIMIENTO (
    id_tipo_mov SERIAL PRIMARY KEY,
    tipo_mov VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS TIPO_INSPECCION (
    id_tipo_inspeccion SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT NULL
);

CREATE TABLE IF NOT EXISTS ESTADO_ALERTA (
    id_estado_alerta SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT NULL
);

-- 2. TABLAS DE UBICACIONES Y BIENES
CREATE TABLE IF NOT EXISTS UBICACION (
    id_ubicacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    id_tipo_ubicacion INT NOT NULL REFERENCES TIPO_UBICACION(id_tipo_ubicacion) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ubicacion_padre INT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS ITEM (
    id_item SERIAL PRIMARY KEY,
    codigo_qr VARCHAR(100) NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT NULL,
    estado VARCHAR(50) NOT NULL DEFAULT 'OPERATIVO',
    cantidad INT NOT NULL DEFAULT 1 CHECK (cantidad >= 0),
    fecha_vencimiento DATE NULL,
    id_categoria INT NOT NULL REFERENCES CATEGORIA_ITEM(id_categoria) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_tipo_item INT NOT NULL REFERENCES TIPO_ITEM(id_tipo_item) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ASIGNACION_ITEMS (
    id_item INT NOT NULL REFERENCES ITEM(id_item) ON UPDATE CASCADE ON DELETE CASCADE,
    id_ubicacion INT NOT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE RESTRICT,
    cantidad_asignada INT NOT NULL DEFAULT 1 CHECK (cantidad_asignada >= 0),
    fecha TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_item, id_ubicacion)
);

-- 3. TABLAS DE TRAZABILIDAD, INSPECCIONES Y ALERTAS
CREATE TABLE IF NOT EXISTS MOVIMIENTO (
    id_movimiento SERIAL PRIMARY KEY,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    fecha TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT NULL,
    id_tipo_mov INT NOT NULL REFERENCES TIPO_MOVIMIENTO(id_tipo_mov) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_item INT NOT NULL REFERENCES ITEM(id_item) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_usuario INT NOT NULL REFERENCES USUARIO(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ubicacion_origen INT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE SET NULL,
    id_ubicacion_destino INT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS INSPECCION (
    id_inspeccion SERIAL PRIMARY KEY,
    fecha TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_tipo_inspeccion INT NOT NULL REFERENCES TIPO_INSPECCION(id_tipo_inspeccion) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_usuario INT NOT NULL REFERENCES USUARIO(id_usuario) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_ubicacion INT NOT NULL REFERENCES UBICACION(id_ubicacion) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS DETALLE_INSPECCION (
    id_detalle SERIAL PRIMARY KEY,
    cantidad_encontrada INT NOT NULL CHECK (cantidad_encontrada >= 0),
    cantidad_teorica_actual INT NOT NULL CHECK (cantidad_teorica_actual >= 0),
    estado_reportado VARCHAR(50) NOT NULL DEFAULT 'OPERATIVO',
    id_inspeccion INT NOT NULL REFERENCES INSPECCION(id_inspeccion) ON UPDATE CASCADE ON DELETE CASCADE,
    id_item INT NOT NULL REFERENCES ITEM(id_item) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS ALERTA_DISCREPANCIA (
    id_alerta SERIAL PRIMARY KEY,
    fecha_generacion TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resuelta BOOLEAN NOT NULL DEFAULT FALSE,
    diferencia INT NOT NULL,
    fecha_resolucion TIMESTAMP WITH TIME ZONE NULL,
    observaciones TEXT NULL,
    id_detalle INT NOT NULL UNIQUE REFERENCES DETALLE_INSPECCION(id_detalle) ON UPDATE CASCADE ON DELETE CASCADE,
    id_estado_alerta INT NOT NULL REFERENCES ESTADO_ALERTA(id_estado_alerta) ON UPDATE CASCADE ON DELETE RESTRICT,
    id_usuario INT NULL REFERENCES USUARIO(id_usuario) ON UPDATE CASCADE ON DELETE SET NULL
);

-- ==============================================================================
-- POBLADO DE DATOS MAESTROS Y SINTÉTICOS DE ALTA FIDELIDAD
-- ==============================================================================

-- Roles Institucionales
INSERT INTO ROL (id_rol, nombre) VALUES 
(1, 'DIRECTOR'),
(2, 'CAPITAN'),
(3, 'TENIENTE'),
(4, 'ENCARGADO_INVENTARIO'),
(5, 'BOMBERO_VOLUNTARIO'),
(6, 'ADMIN_PORTAL')
ON CONFLICT (id_rol) DO UPDATE SET nombre = EXCLUDED.nombre;

-- Usuarios Oficiales del Cuartel
INSERT INTO USUARIO (id_usuario, id_voluntario, nombre, email, id_rol) VALUES
(1, 101, 'Cristian Jiménez Fuentes', 'cristian.jimenez2201@alumnos.ubiobio.cl', 1),
(2, 102, 'Matías Aguilera Ibarra', 'matias.aguilera@alumnos.ubiobio.cl', 2),
(3, 103, 'Teniente Primero Juan Rivas', 'teniente1@bomberoschillanviejo.cl', 3),
(4, 104, 'Encargado Pedro Morales', 'inventario@bomberoschillanviejo.cl', 4),
(5, 105, 'Voluntario Diego Carrasco', 'voluntario1@bomberoschillanviejo.cl', 5)
ON CONFLICT (id_usuario) DO UPDATE SET nombre = EXCLUDED.nombre, email = EXCLUDED.email, id_rol = EXCLUDED.id_rol;

-- Clasificación de Ítems
INSERT INTO TIPO_ITEM (id_tipo_item, tipo_clasificacion) VALUES 
(1, 'AGRUPABLE_LOTE'),
(2, 'UNITARIO_ETIQUETABLE')
ON CONFLICT (id_tipo_item) DO UPDATE SET tipo_clasificacion = EXCLUDED.tipo_clasificacion;

-- Categorías
INSERT INTO CATEGORIA_ITEM (id_categoria, nombre) VALUES 
(1, 'Mobiliario y Cuartel'),
(2, 'Herramientas Menores'),
(3, 'Equipos de Proteccion Personal (EPP)'),
(4, 'Insumos Medicos y Botiquin'),
(5, 'Cocina y Aseo'),
(6, 'Vehiculos y Material Mayor'),
(7, 'Tecnologia y Comunicaciones')
ON CONFLICT (id_categoria) DO UPDATE SET nombre = EXCLUDED.nombre;

-- Tipos de Ubicación
INSERT INTO TIPO_UBICACION (id_tipo_ubicacion, tipo) VALUES 
(1, 'CARRO_BOMBA'),
(2, 'BODEGA_CENTRAL'),
(3, 'CABANA_PANOL'),
(4, 'COMPARTIMENTO_CORTINA'),
(5, 'ESTANTE_BODEGA')
ON CONFLICT (id_tipo_ubicacion) DO UPDATE SET tipo = EXCLUDED.tipo;

-- Tipos de Movimiento
INSERT INTO TIPO_MOVIMIENTO (id_tipo_mov, tipo_mov) VALUES 
(1, 'ALTA_COMPRA'),
(2, 'ALTA_DONACION'),
(3, 'TRASLADO'),
(4, 'DEVOLUCION'),
(5, 'EXTRAVIO_EMERGENCIA'),
(6, 'BAJA_DETERIORO'),
(7, 'RECUPERACION_POST_SINIESTRO'),
(8, 'AJUSTE_INVENTARIO')
ON CONFLICT (id_tipo_mov) DO UPDATE SET tipo_mov = EXCLUDED.tipo_mov;

-- Tipos de Inspección
INSERT INTO TIPO_INSPECCION (id_tipo_inspeccion, nombre, descripcion) VALUES 
(1, 'RUTINARIA_PERIODICA', 'Inspeccion programada y mantenimiento semanal/mensual'),
(2, 'POST_EMERGENCIA', 'Recuento rapido tras retorno de acto de servicio o siniestro')
ON CONFLICT (id_tipo_inspeccion) DO UPDATE SET nombre = EXCLUDED.nombre, descripcion = EXCLUDED.descripcion;

-- Estados de Alerta
INSERT INTO ESTADO_ALERTA (id_estado_alerta, nombre, descripcion) VALUES 
(1, 'PENDIENTE', 'Discrepancia detectada en terreno, en espera de revision oficial'),
(2, 'RESUELTA_HALLAZGO', 'Material localizado internamente sin merma patrimonial'),
(3, 'CONFIRMADA_EXTRAVIO', 'Perdida definitiva ratificada tras siniestro multi-compania'),
(4, 'TRAMITADA_BAJA', 'Material danado e inutilizado derivado a proceso formal de baja'),
(5, 'DESCARTADA', 'Error de digitacion o falsa alarma durante el conteo')
ON CONFLICT (id_estado_alerta) DO UPDATE SET nombre = EXCLUDED.nombre, descripcion = EXCLUDED.descripcion;

-- 4. UBICACIONES JERÁRQUICAS (CARROS, BODEGAS Y COMPARTIMENTOS)
-- Ubicaciones Principales
INSERT INTO UBICACION (id_ubicacion, nombre, descripcion, id_tipo_ubicacion, id_ubicacion_padre) VALUES
(1, 'Carro Bomba B-6', 'Unidad de primera intervencion y agua (Renault Camiva)', 1, NULL),
(2, 'Unidad de Rescate R-6', 'Unidad de rescate vehicular y extricacion pesada', 1, NULL),
(3, 'Bodega Central del Cuartel', 'Bodega general de abastecimiento y reserva', 2, NULL)
ON CONFLICT (id_ubicacion) DO UPDATE SET nombre = EXCLUDED.nombre, descripcion = EXCLUDED.descripcion;

-- Compartimentos Carro B-6
INSERT INTO UBICACION (id_ubicacion, nombre, descripcion, id_tipo_ubicacion, id_ubicacion_padre) VALUES
(4, 'Cabina Conductor (B-6)', 'Equipos portatiles de comunicacion y mando', 4, 1),
(5, 'Cortina Izquierda 1 (B-6)', 'Gaveta de ataque rapido y mangueras 70mm', 4, 1),
(6, 'Cortina Izquierda 2 (B-6)', 'Herramientas de entrada forzada y motobomba', 4, 1),
(7, 'Cortina Derecha 1 (B-6)', 'Alimentacion, bifurcaciones y pitones', 4, 1),
(8, 'Techo y Bandeja (B-6)', 'Escalas de corredera y manguerotes de succion', 4, 1)
ON CONFLICT (id_ubicacion) DO UPDATE SET nombre = EXCLUDED.nombre;

-- Compartimentos Carro R-6
INSERT INTO UBICACION (id_ubicacion, nombre, descripcion, id_tipo_ubicacion, id_ubicacion_padre) VALUES
(9, 'Cabina Rescate (R-6)', 'Botiquines trauma y chalecos de extricacion', 4, 2),
(10, 'Gaveta Hidraulica (R-6)', 'Cizalla, separador y unidad de poder Holmatro', 4, 2),
(11, 'Gaveta Cuerdas y Altura (R-6)', 'Cuerdas semiestaticas, mosquetones y arneses', 4, 2)
ON CONFLICT (id_ubicacion) DO UPDATE SET nombre = EXCLUDED.nombre;

-- Zonas Bodega Central
INSERT INTO UBICACION (id_ubicacion, nombre, descripcion, id_tipo_ubicacion, id_ubicacion_padre) VALUES
(12, 'Panol de Herramientas (Bodega)', 'Sector de mantencion y reserva de motobombas', 3, 3),
(13, 'Estante EPP y Uniformes (Bodega)', 'Cascos, uniformes estructurales y botas de recambio', 5, 3),
(14, 'Estante Insumos Medicos (Bodega)', 'Apositos, cuellos cervicales y gasas', 5, 3)
ON CONFLICT (id_ubicacion) DO UPDATE SET nombre = EXCLUDED.nombre;

-- 5. CATÁLOGO DE BIENES (25+ ACTIVOS DE ALTA FIDELIDAD)
INSERT INTO ITEM (id_item, codigo_qr, nombre, descripcion, estado, cantidad, fecha_vencimiento, id_categoria, id_tipo_item) VALUES
-- Mangueras y Pitones (Agrupables)
(1, NULL, 'Manguera Sintetica 70mm x 25m', 'Manguera semirrigida color naranja de alto caudal', 'OPERATIVO', 20, NULL, 2, 1),
(2, NULL, 'Manguera Sintetica 50mm x 25m', 'Manguera de ataque color amarillo de media presion', 'OPERATIVO', 24, NULL, 2, 1),
(3, NULL, 'Piton Triple Efecto 50mm Protek', 'Piton de caudal variable con boquilla de chorro/niebla', 'OPERATIVO', 6, NULL, 2, 1),
(4, NULL, 'Bifurcacion 70mm a 2x50mm', 'Bifurcador con valvulas de bola independientes', 'OPERATIVO', 4, NULL, 2, 1),
(5, NULL, 'Hacha Pico-Plana de Bombero', 'Hacha de acero forjado con mango dielectrico', 'OPERATIVO', 5, NULL, 2, 1),
(6, NULL, 'Halligan Tool Entrada Forzada', 'Barra multiproposito de acero aleado', 'OPERATIVO', 3, NULL, 2, 1),

-- Equipos Motorizados y Tecnológicos (Unitarios con QR)
(7, 'QR-MOTO-001', 'Motosierra Stihl MS 362 C-M', 'Motosierra de rescate y ventilacion 59cc', 'OPERATIVO', 1, NULL, 2, 2),
(8, 'QR-GEN-001', 'Generador Electrico Honda EU22i', 'Generador insonorizado inverter 2.2 kVA', 'OPERATIVO', 1, NULL, 2, 2),
(9, 'QR-BOM-001', 'Motobomba de Caudal Honda WT30X', 'Bomba para aguas sucias 1200 L/min', 'OPERATIVO', 1, NULL, 2, 2),
(10, 'QR-RAD-001', 'Radio Portatil Motorola APX 2000', 'Radio troncalizada VHF P25 sumergible', 'OPERATIVO', 1, NULL, 7, 2),
(11, 'QR-RAD-002', 'Radio Portatil Motorola APX 2000', 'Radio troncalizada VHF P25 sumergible', 'OPERATIVO', 1, NULL, 7, 2),
(12, 'QR-RAD-003', 'Radio Portatil Motorola APX 2000', 'Radio troncalizada VHF P25 sumergible', 'OPERATIVO', 1, NULL, 7, 2),

-- Rescate Vehicular e Hidráulico (Unitarios con QR)
(13, 'QR-HOL-001', 'Cizalla Hidraulica Holmatro CU 5050', 'Herramienta de corte vehicular alta potencia', 'OPERATIVO', 1, NULL, 2, 2),
(14, 'QR-HOL-002', 'Separador Hidraulico Holmatro SP 5240', 'Herramienta de apertura vehicular 725mm', 'OPERATIVO', 1, NULL, 2, 2),
(15, 'QR-VET-001', 'Cojin de Levante Neumatico Vetter 24T', 'Cojin de alta presion para rescate pesado', 'OPERATIVO', 1, NULL, 2, 2),

-- EPP y Equipos de Respiración (Unitarios con QR y Agrupables)
(16, 'QR-ERA-001', 'Equipo ERA Scott Air-Pak 75 4.5', 'Equipo de respiracion autonoma con mascara AV-3000', 'OPERATIVO', 1, '2028-12-31', 3, 2),
(17, 'QR-ERA-002', 'Equipo ERA Scott Air-Pak 75 4.5', 'Equipo de respiracion autonoma con mascara AV-3000', 'OPERATIVO', 1, '2028-12-31', 3, 2),
(18, 'QR-CAS-001', 'Casco Estructural MSA Gallet F1 XF', 'Casco integral con visor dorado y linterna integrada', 'OPERATIVO', 1, NULL, 3, 2),
(19, 'QR-CAS-002', 'Casco Estructural MSA Gallet F1 XF', 'Casco integral con visor dorado y linterna integrada', 'OPERATIVO', 1, NULL, 3, 2),
(20, NULL, 'Guantes de Estructura Dragon Fire', 'Guantes de cuero hidrofugado certificados NFPA', 'OPERATIVO', 10, NULL, 3, 1),

-- Extintores e Insumos Médicos
(21, 'QR-EXT-001', 'Extintor Polvo Quimico Seco 10kg ABC', 'Extintor presurizado con manometro certificado', 'OPERATIVO', 1, '2026-11-30', 2, 2),
(22, 'QR-EXT-002', 'Extintor Polvo Quimico Seco 10kg ABC', 'Extintor presurizado con manometro certificado', 'OPERATIVO', 1, '2026-11-30', 2, 2),
(23, 'QR-EXT-003', 'Extintor CO2 5kg Nieve Carbonica', 'Extintor para tableros electricos y cabina', 'OPERATIVO', 1, '2027-03-31', 2, 2),
(24, 'QR-BOT-001', 'Botiquin Trauma Avanzado Orange', 'Mochila de soporte vital con oxigenoterapia portatil', 'OPERATIVO', 1, NULL, 4, 2),
(25, NULL, 'Collar Cervical Regulable Adulto Laerdal', 'Inmovilizador cervical pediatrico y adulto', 'OPERATIVO', 8, NULL, 4, 1),
(26, NULL, 'Tabla Espinal Larga con Inmovilizador', 'Camilla rigida de polietileno flotante', 'OPERATIVO', 3, NULL, 4, 1)
ON CONFLICT (id_item) DO UPDATE SET nombre = EXCLUDED.nombre, cantidad = EXCLUDED.cantidad;

-- 6. ASIGNACIONES DE STOCK FÍSICO POR UBICACIÓN
INSERT INTO ASIGNACION_ITEMS (id_item, id_ubicacion, cantidad_asignada) VALUES
-- Carro B-6: Cortina Izq 1
(1, 5, 8),   -- 8 mangueras 70mm
(2, 5, 10),  -- 10 mangueras 50mm
(3, 5, 2),   -- 2 pitones 50mm

-- Carro B-6: Cortina Izq 2
(5, 6, 2),   -- 2 hachas pico-plana
(6, 6, 1),   -- 1 halligan tool
(7, 6, 1),   -- 1 motosierra Stihl (QR-MOTO-001)

-- Carro B-6: Cortina Der 1
(1, 7, 4),   -- 4 mangueras 70mm
(2, 7, 6),   -- 6 mangueras 50mm
(4, 7, 2),   -- 2 bifurcaciones
(21, 7, 1),  -- 1 extintor PQS 10kg (QR-EXT-001)

-- Carro B-6: Cabina
(10, 4, 1),  -- 1 radio Motorola (QR-RAD-001)
(11, 4, 1),  -- 1 radio Motorola (QR-RAD-002)
(16, 4, 1),  -- 1 ERA Scott (QR-ERA-001)
(17, 4, 1),  -- 1 ERA Scott (QR-ERA-002)
(23, 4, 1),  -- 1 extintor CO2 (QR-EXT-003)

-- Carro R-6: Gaveta Hidráulica
(13, 10, 1), -- 1 cizalla Holmatro (QR-HOL-001)
(14, 10, 1), -- 1 separador Holmatro (QR-HOL-002)
(15, 10, 1), -- 1 cojin Vetter (QR-VET-001)
(8, 10, 1),  -- 1 generador Honda (QR-GEN-001)

-- Carro R-6: Cabina
(12, 9, 1),  -- 1 radio Motorola (QR-RAD-003)
(24, 9, 1),  -- 1 botiquin trauma (QR-BOT-001)
(25, 9, 3),  -- 3 collares cervicales
(26, 9, 2),  -- 2 tablas espinales

-- Bodega Central: Stock de Reserva
(1, 12, 8),  -- 8 mangueras 70mm
(2, 12, 8),  -- 8 mangueras 50mm
(9, 12, 1),  -- 1 motobomba Honda (QR-BOM-001)
(18, 13, 1), -- 1 casco Gallet F1 (QR-CAS-001)
(19, 13, 1), -- 1 casco Gallet F1 (QR-CAS-002)
(20, 13, 10),-- 10 guantes de estructura
(22, 12, 1), -- 1 extintor PQS de reserva (QR-EXT-002)
(25, 14, 5), -- 5 collares cervicales
(26, 14, 1)  -- 1 tabla espinal
ON CONFLICT (id_item, id_ubicacion) DO UPDATE SET cantidad_asignada = EXCLUDED.cantidad_asignada;

-- 7. MOVIMIENTOS HISTÓRICOS DE EJEMPLO (LEDGER INMUTABLE)
INSERT INTO MOVIMIENTO (id_movimiento, cantidad, id_tipo_mov, id_item, id_usuario, id_ubicacion_origen, id_ubicacion_destino, observaciones, fecha) VALUES
(1, 20, 1, 1, 1, NULL, 3, 'Adquisicion institucional de 20 mangueras 70mm segun factura N 4892', NOW() - INTERVAL '30 days'),
(2, 8, 3, 1, 4, 3, 5, 'Distribucion inicial de 8 mangueras 70mm hacia Carro B-6 Cortina Izquierda 1', NOW() - INTERVAL '25 days'),
(3, 4, 3, 1, 4, 3, 7, 'Distribucion de 4 mangueras 70mm hacia Carro B-6 Cortina Derecha 1', NOW() - INTERVAL '25 days'),
(4, 1, 1, 7, 1, NULL, 6, 'Compra y asignacion de Motosierra Stihl a Carro B-6', NOW() - INTERVAL '20 days'),
(5, 1, 1, 13, 1, NULL, 10, 'Recepcion de equipo de rescate pesado Holmatro para Unidad R-6', NOW() - INTERVAL '15 days')
ON CONFLICT (id_movimiento) DO NOTHING;

-- 8. INSPECCIÓN SINTÉTICA CON ALERTA DE DISCREPANCIA ACTIVA
INSERT INTO INSPECCION (id_inspeccion, id_tipo_inspeccion, id_usuario, id_ubicacion, fecha) VALUES
(1, 2, 2, 1, NOW() - INTERVAL '2 hours')
ON CONFLICT (id_inspeccion) DO NOTHING;

INSERT INTO DETALLE_INSPECCION (id_detalle, id_inspeccion, id_item, cantidad_encontrada, cantidad_teorica_actual, estado_reportado) VALUES
(1, 1, 1, 8, 8, 'OPERATIVO'),
(2, 1, 5, 1, 2, 'OPERATIVO') -- Faltante: Se encontraron 1 de 2 hachas (Alerta Crítica)
ON CONFLICT (id_detalle) DO NOTHING;

INSERT INTO ALERTA_DISCREPANCIA (id_alerta, id_detalle, id_estado_alerta, id_usuario, diferencia, resuelta, observaciones, fecha_generacion) VALUES
(1, 2, 1, NULL, -1, FALSE, 'Falta 1 Hacha Pico-Plana tras llamado 10-0-1 en Calle O Higgins con Maipu. Posible extravio en terreno multi-compania.', NOW() - INTERVAL '2 hours')
ON CONFLICT (id_alerta) DO NOTHING;
