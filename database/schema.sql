-- Actualizacion de Base de Datos (V2)

-- Expandiendo la tabla habitacion
DROP TABLE IF EXISTS factura CASCADE;
DROP TABLE IF EXISTS reserva CASCADE;
DROP TABLE IF EXISTS habitacion CASCADE;

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

INSERT INTO habitacion (numero, piso, tipo, vista, precio_bs, estado) VALUES
('101', 1, 'Simple', 'Interior', 150.00, 'disponible'),
('102', 1, 'Simple', 'A la Calle', 180.00, 'disponible'),
('201', 2, 'Doble Twin', 'A la Calle', 250.00, 'disponible'),
('301', 3, 'Matrimonial', 'Interior', 300.00, 'disponible'),
('501', 5, 'Suite Ejecutiva', 'Al Illimani', 500.00, 'disponible');

