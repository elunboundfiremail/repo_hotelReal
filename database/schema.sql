-- Esquema Completo de Base de Datos - Hotel Real

DROP TABLE IF EXISTS factura CASCADE;
DROP TABLE IF EXISTS reserva CASCADE;
DROP TABLE IF EXISTS habitacion CASCADE;
DROP TABLE IF EXISTS perfil_cliente CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('admin', 'cliente')),
    correo VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE perfil_cliente (
    id_usuario INTEGER PRIMARY KEY REFERENCES usuario(id),
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    ci VARCHAR(20) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    nit VARCHAR(20),
    razon_social VARCHAR(100)
);

CREATE TABLE habitacion (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL,
    piso INTEGER NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    vista VARCHAR(50) DEFAULT 'Interior' CHECK (vista IN ('Interior', 'A la Calle', 'Al Illimani')),
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

-- Insercion de datos por defecto
INSERT INTO usuario (rol, correo, password_hash) VALUES ('admin', 'admin@hotelreal.com.bo', 'admin123');

INSERT INTO habitacion (numero, piso, tipo, vista, precio_bs, estado) VALUES
('101', 1, 'Simple', 'Interior', 150.00, 'disponible'),
('102', 1, 'Simple', 'A la Calle', 180.00, 'disponible'),
('201', 2, 'Doble Twin', 'A la Calle', 250.00, 'disponible'),
('301', 3, 'Matrimonial', 'Interior', 300.00, 'disponible'),
('501', 5, 'Suite Ejecutiva', 'Al Illimani', 500.00, 'disponible');
