from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import shutil

app = FastAPI(title="Hotel Real API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    "dbname": "db_hotelreal",
    "user": "admin_db_hotel",
    "password": "hotel123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print("Error de BD:", e)
        return None

# Directorio de reportes/comprobantes (Debe coincidir con la configuracion de Linux)
UPLOAD_DIR = "/var/hotel_reportes"
if not os.path.exists(UPLOAD_DIR):
    # Fallback local para pruebas si no hay permisos aun
    UPLOAD_DIR = "./comprobantes_temp"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

class LoginRequest(BaseModel):
    correo: str
    password: str

class RegistroRequest(BaseModel):
    nombre: str
    apellido_paterno: str
    apellido_materno: str
    ci: str
    telefono: str
    correo: str
    password: str

@app.post("/api/registro")
def registro(req: RegistroRequest):
    conn = get_db_connection()
    if not conn: raise HTTPException(status_code=500)
    cursor = conn.cursor()
    try:
        # Insertar usuario (cliente)
        cursor.execute("INSERT INTO usuario (rol, correo, password_hash) VALUES ('cliente', %s, %s) RETURNING id", (req.correo, req.password))
        user_id = cursor.fetchone()[0]
        # Insertar perfil
        cursor.execute("INSERT INTO perfil_cliente (id_usuario, nombre, apellido_paterno, apellido_materno, ci, telefono) VALUES (%s, %s, %s, %s, %s, %s)",
                       (user_id, req.nombre, req.apellido_paterno, req.apellido_materno, req.ci, req.telefono))
        conn.commit()
        return {"mensaje": "Registro exitoso", "user_id": user_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Error en registro. El correo o CI ya existen.")
    finally:
        cursor.close()
        conn.close()

@app.post("/api/login")
def login(req: LoginRequest):
    conn = get_db_connection()
    if not conn: raise HTTPException(status_code=500)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, rol FROM usuario WHERE correo = %s AND password_hash = %s", (req.correo, req.password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return {"mensaje": "Login exitoso", "usuario": user}
    raise HTTPException(status_code=401, detail="Credenciales invalidas")

@app.get("/api/habitaciones")
def get_habitaciones():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # Agrupar por tipo para la pagina principal
    cursor.execute("SELECT DISTINCT ON (tipo) tipo, precio_bs FROM habitacion WHERE estado = 'disponible'")
    habs = cursor.fetchall()
    cursor.close()
    conn.close()
    return habs

@app.get("/api/habitaciones/detalle")
def get_habitaciones_detalle(tipo: str = None):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM habitacion WHERE estado = 'disponible'"
    params = []
    if tipo:
        query += " AND tipo = %s"
        params.append(tipo)
    cursor.execute(query, params)
    habs = cursor.fetchall()
    cursor.close()
    conn.close()
    return habs

@app.post("/api/reservar")
def hacer_reserva(
    id_usuario: int = Form(...),
    id_habitacion: int = Form(...),
    fecha_entrada: str = Form(...),
    fecha_salida: str = Form(...),
    comprobante: UploadFile = File(...)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Guardar imagen físicamente
        file_path = f"{UPLOAD_DIR}/user{id_usuario}_hab{id_habitacion}_{comprobante.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(comprobante.file, buffer)
        
        # Guardar en BD
        cursor.execute("""
            INSERT INTO reserva (id_usuario, id_habitacion, fecha_entrada, fecha_salida, estado_pago, ruta_comprobante)
            VALUES (%s, %s, %s, %s, 'verificando', %s) RETURNING id
        """, (id_usuario, id_habitacion, fecha_entrada, fecha_salida, file_path))
        reserva_id = cursor.fetchone()[0]
        
        # Marcar habitacion como ocupada
        cursor.execute("UPDATE habitacion SET estado = 'ocupada' WHERE id = %s", (id_habitacion,))
        conn.commit()
        return {"mensaje": "Reserva creada. En verificacion.", "reserva_id": reserva_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/api/admin/reservas")
def get_reservas_admin():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT r.id, r.fecha_entrada, r.fecha_salida, r.estado_pago, h.numero, h.piso, h.tipo, p.nombre, p.apellido_paterno
        FROM reserva r
        JOIN habitacion h ON r.id_habitacion = h.id
        JOIN perfil_cliente p ON r.id_usuario = p.id_usuario
        ORDER BY r.fecha_entrada DESC
    """)
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return reservas

@app.post("/api/admin/aprobar/{reserva_id}")
def aprobar_reserva(reserva_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Aprobar
        cursor.execute("UPDATE reserva SET estado_pago = 'pagado' WHERE id = %s", (reserva_id,))
        # Crear Factura automaticamente (Generacion simple para el informe)
        cursor.execute("""
            INSERT INTO factura (id_reserva, nit_emision, razon_social_emision, monto_total)
            SELECT r.id, COALESCE(p.nit, '123456789'), COALESCE(p.razon_social, p.nombre || ' ' || p.apellido_paterno), h.precio_bs
            FROM reserva r
            JOIN habitacion h ON r.id_habitacion = h.id
            JOIN perfil_cliente p ON r.id_usuario = p.id_usuario
            WHERE r.id = %s
        """, (reserva_id,))
        conn.commit()
        return {"mensaje": "Aprobada y Factura Generada"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/api/cliente/reservas/{usuario_id}")
def get_reservas_cliente(usuario_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT r.id, r.fecha_entrada, r.fecha_salida, r.estado_pago, h.numero, h.tipo, h.precio_bs
        FROM reserva r
        JOIN habitacion h ON r.id_habitacion = h.id
        WHERE r.id_usuario = %s
    """, (usuario_id,))
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return reservas
