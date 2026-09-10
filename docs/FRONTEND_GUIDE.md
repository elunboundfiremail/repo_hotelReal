# Guía del Frontend

El Frontend es la interfaz gráfica de usuario donde Recepción visualizará el estado de las habitaciones.

## Arquitectura y Tecnologías
- **HTML5:** Estructura semántica.
- **Tailwind CSS:** Framework de diseño utilitario (importado vía CDN) para un diseño minimalista, moderno y responsivo (UI/UX).
- **Vanilla JavaScript:** Lógica asíncrona (`fetch`) para conectarse al backend y pintar el DOM dinámicamente.

## Estructura de Directorios
Se encuentra en `src/frontend/`:
- `index.html`: Vista principal.
- `css/styles.css`: Clases personalizadas (Glassmorphism y animaciones).
- `js/app.js`: Script que llama al endpoint `/api/rooms` del Backend.

## Cómo Levantarlo (Ejecución)
Al ser una aplicación basada en Vanilla JS sin frameworks pesados como React o Angular, **no necesitas un servidor Node.js ni compilar nada**.

1. **Desarrollo Local:** 
   Simplemente haz doble clic en `index.html` para abrirlo en cualquier navegador web.
2. **Producción (En el Servidor Linux):**
   Deberás copiar el contenido de la carpeta `src/frontend/` a la ruta `/var/www/html/` para que Nginx o Apache lo sirvan por el puerto 80.
