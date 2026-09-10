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

---

## 🚀 Cómo Levantar el Backend (Paso a Paso)

Para que la página web funcione, el motor (Backend) debe estar encendido y corriendo de fondo. 

1. Abre tu **Terminal** (recomendado usar la terminal integrada de VS Code).
2. Entra a la carpeta del backend:
   ```bash
   cd /home/user/proyecto_so2_hotel/src/backend
   ```
3. Ejecuta el archivo principal usando el entorno virtual que tiene instalado FastAPI:
   ```bash
   ../../venv/bin/python3 main.py
   ```
4. Verás un mensaje en verde confirmando que el servidor ha iniciado.
5. **Verificación:** Abre tu navegador de Ubuntu y entra a:
   - Para ver la API gráfica (Swagger): [http://localhost:8080/docs](http://localhost:8080/docs)
   - Para ver los datos crudos en JSON: [http://localhost:8080/api/rooms](http://localhost:8080/api/rooms)

*(Nota: Para apagar el servidor, simplemente presiona `Ctrl + C` en la terminal).*
