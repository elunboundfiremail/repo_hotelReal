# Guía del Backend y Base de Datos

El Backend es el motor lógico del hotel. Expone la información de PostgreSQL hacia el Frontend a través de una API REST.

## Arquitectura y Tecnologías
- **Python 3.12**
- **FastAPI:** Framework de alto rendimiento con auto-documentación (Swagger).
- **Psycopg2:** Driver conector para comunicarse nativamente con PostgreSQL.
- **Estructura N-Capas:** Separación de controladores (`api/`), lógica (`services/`) y acceso a datos (`db/`).

## Configuración de PostgreSQL
La base de datos se llama `hotel_real`. Las credenciales configuradas en `src/backend/db/connection.py` son:
* **User:** postgres
* **Password:** admin123
* **Host/Port:** localhost:5432

## Cómo Levantarlo (Ejecución)

1. Abre tu terminal en la raíz del proyecto (`/home/user/proyecto_so2_hotel/`).
2. Activa el entorno virtual (o usa directamente su binario):
   ```bash
   ./venv/bin/python3 src/backend/main.py
   ```
3. El servidor iniciará en el puerto `8080`.
4. **Ver el Swagger UI:** Entra a `http://localhost:8080/docs` en tu navegador para ver la documentación gráfica interactiva de la API.
