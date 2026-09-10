-- Consultas de prueba para PostgreSQL
-- Para ejecutar, entra a PostgreSQL con: sudo -u postgres psql -d hotel_real

-- 1. Ver todas las habitaciones y su estado actual
SELECT id, room_number, room_type, status FROM rooms ORDER BY room_number ASC;

-- 2. Ver solo las habitaciones disponibles para Recepcion
SELECT room_number, room_type FROM rooms WHERE status = 'available';

-- 3. Marcar una habitación (ej. 102) como ocupada (Simulando un Check-in)
UPDATE rooms SET status = 'occupied' WHERE room_number = 102;

-- 4. Marcar una habitación (ej. 104) como libre (Simulando un Check-out)
UPDATE rooms SET status = 'available' WHERE room_number = 104;

-- 5. Poner una habitación en mantenimiento
UPDATE rooms SET status = 'maintenance' WHERE room_number = 201;

-- 6. Contar cuántas habitaciones están libres vs ocupadas
SELECT status, COUNT(*) as total FROM rooms GROUP BY status;
