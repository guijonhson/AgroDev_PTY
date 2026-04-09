-- ===============================
-- AgroDev – Sistema de Gestión Agropecuaria
-- Base de Datos SQLite (MVP)
-- ===============================

PRAGMA foreign_keys = ON;

-- ===============================
-- 1. PRODUCTOR
-- ===============================
CREATE TABLE IF NOT EXISTS productor (
    id_productor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    correo TEXT,
    fecha_creacion DATE DEFAULT CURRENT_DATE
);

-- ===============================
-- 2. USUARIO
-- ===============================
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_productor INTEGER NOT NULL,
    nombre_usuario TEXT NOT NULL,
    correo TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL,
    activo INTEGER DEFAULT 1,
    FOREIGN KEY (id_productor) REFERENCES productor(id_productor)
);

-- ===============================
-- 3. FINCA
-- ===============================
CREATE TABLE IF NOT EXISTS finca (
    id_finca INTEGER PRIMARY KEY AUTOINCREMENT,
    id_productor INTEGER NOT NULL,
    nombre_finca TEXT NOT NULL,
    ubicacion TEXT,
    area_total REAL,
    FOREIGN KEY (id_productor) REFERENCES productor(id_productor)
);

-- ===============================
-- 4. PARCELA
-- ===============================
CREATE TABLE IF NOT EXISTS parcela (
    id_parcela INTEGER PRIMARY KEY AUTOINCREMENT,
    id_finca INTEGER NOT NULL,
    numero_parcela TEXT NOT NULL,
    area REAL,
    FOREIGN KEY (id_finca) REFERENCES finca(id_finca)
);

-- ===============================
-- 5. CULTIVO
-- ===============================
CREATE TABLE IF NOT EXISTS cultivo (
    id_cultivo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_cultivo TEXT NOT NULL,
    ciclo_dias_aprox INTEGER
);

-- ===============================
-- 6. PRODUCTO (INSUMOS)
-- ===============================
CREATE TABLE IF NOT EXISTS producto (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_producto TEXT NOT NULL,
    tipo_producto TEXT NOT NULL
);

-- ===============================
-- 7. APLICADOR
-- ===============================
CREATE TABLE IF NOT EXISTS aplicador (
    id_aplicador INTEGER PRIMARY KEY AUTOINCREMENT,
    id_productor INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    cargo TEXT,
    FOREIGN KEY (id_productor) REFERENCES productor(id_productor)
);

-- ===============================
-- 8. REGISTRO AGRÍCOLA
-- ===============================
CREATE TABLE IF NOT EXISTS registro_agricola (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    id_cultivo INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    tipo_control TEXT NOT NULL,
    dosis REAL NOT NULL,
    id_parcela INTEGER NOT NULL,
    id_aplicador INTEGER NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (id_cultivo) REFERENCES cultivo(id_cultivo),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
    FOREIGN KEY (id_parcela) REFERENCES parcela(id_parcela),
    FOREIGN KEY (id_aplicador) REFERENCES aplicador(id_aplicador)
);

-- ===============================
-- 9. PLAN DE SUSCRIPCIÓN
-- ===============================
CREATE TABLE IF NOT EXISTS plan (
    id_plan INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_plan TEXT NOT NULL,
    precio_mensual REAL NOT NULL,
    descripcion TEXT,
    activo INTEGER DEFAULT 1
);

-- ===============================
-- 10. SUSCRIPCIÓN
-- ===============================
CREATE TABLE IF NOT EXISTS suscripcion (
    id_suscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_productor INTEGER NOT NULL,
    id_plan INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado TEXT NOT NULL,
    FOREIGN KEY (id_productor) REFERENCES productor(id_productor),
    FOREIGN KEY (id_plan) REFERENCES plan(id_plan)
);

-- ===============================
-- 11. PAGOS
-- ===============================
CREATE TABLE IF NOT EXISTS pago (
    id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    id_suscripcion INTEGER NOT NULL,
    fecha_pago DATE NOT NULL,
    monto REAL NOT NULL,
    metodo_pago TEXT,
    referencia TEXT,
    estado TEXT NOT NULL,
    FOREIGN KEY (id_suscripcion) REFERENCES suscripcion(id_suscripcion)
);
