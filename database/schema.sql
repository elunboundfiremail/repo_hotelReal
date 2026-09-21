-- Script de creacion de Base de Datos para Hotel Real
-- Cumpliendo con 3FN y reglas estrictas (sin acentos)

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'cliente')),
    correo VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE perfil_cliente (
    id_usuario INTEGER PRIMARY KEY REFERENCES usuario(id) ON DELETE CASCADE,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    ci VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    nit VARCHAR(20),
    razon_social VARCHAR(100)
);

CREATE TABLE habitacion (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    precio_bs DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'disponible' CHECK (estado IN ('disponible', 'ocupada', 'mantenimiento'))
);

CREATE TABLE reserva (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuario(id),
    id_habitacion INTEGER REFERENCES habitacion(id),
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    estado_pago VARCHAR(20) DEFAULT 'pendiente' CHECK (estado_pago IN ('pendiente', 'verificando', 'pagado', 'rechazado')),
    ruta_comprobante VARCHAR(255)
);

CREATE TABLE factura (
    id SERIAL PRIMARY KEY,
    id_reserva INTEGER REFERENCES reserva(id),
    nit_emision VARCHAR(20) NOT NULL,
    razon_social_emision VARCHAR(100) NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos iniciales
INSERT INTO habitacion (tipo, precio_bs, estado) VALUES
('Simple', 150.00, 'disponible'),
('Simple', 150.00, 'disponible'),
('Doble Twin', 250.00, 'disponible'),
('Matrimonial', 300.00, 'disponible'),
('Suite Ejecutiva', 500.00, 'disponible');
