from db.connection import get_db_connection
from psycopg2.extras import RealDictCursor

def fetch_all_rooms():
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, room_number AS id, room_type AS type, status FROM rooms ORDER BY room_number ASC;")
            return cursor.fetchall()
    finally:
        conn.close()
