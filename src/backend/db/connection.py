import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException

DB_CONFIG = {
    "dbname": "hotel_real",
    "user": "postgres",
    "password": "admin123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
