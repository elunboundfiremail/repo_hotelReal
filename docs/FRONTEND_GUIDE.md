# Guía del Frontend

El Frontend es la interfaz gráfica de usuario donde Recepción visualizará el estado de las habitaciones.

## Arquitectura y Tecnologías
- **HTML5:** Estructura semántica.
- **Tailwind CSS:** Framework de diseño utilitario (importado vía CDN) para un diseño minimalista, moderno y responsivo (UI/UX).
- **Vanilla JavaScript:** Lógica asíncrona (`fetch`) para conectarse al backend y pintar el DOM dinámicamente.

## Estructura de Directorios
Se encuentra en `src/frontend/`:
- `index.html`: Vista principal.
- `css/styles.css`: Clases personalizadas.
- `js/app.js`: Script que llama al endpoint `/api/rooms`.

---

## 🚀 Cómo Levantar el Frontend (Paso a Paso)

A diferencia del Backend, este Frontend es totalmente ligero. No necesitas instalar Node.js ni compilar nada para visualizarlo.

**IMPORTANTE:** Asegúrate de que el Backend ya esté corriendo (revisa la guía del backend) antes de abrir el Frontend, o de lo contrario verás un error de conexión.

### Opción 1: Por Terminal (Recomendado)
Abre una terminal nueva y usa el comando nativo de Ubuntu para abrir la web:
```bash
xdg-open /home/user/proyecto_so2_hotel/src/frontend/index.html
```

### Opción 2: Gráficamente con el Ratón
1. Abre tu **Explorador de Archivos** normal de Ubuntu.
2. Navega hasta la ruta: `proyecto_so2_hotel` > `src` > `frontend`.
3. Haz doble clic sobre el archivo **`index.html`**.
4. Se abrirá automáticamente tu navegador web por defecto (ej. Firefox) mostrando la interfaz conectada a tu Base de Datos.

---

### Producción (Fase de Servidor Linux)
El día de la defensa, para que este frontend se vea en red local (ej. entrando a `hotelreal.local`), deberás copiar el contenido de esta carpeta `frontend` hacia `/var/www/html/` para que tu servidor web Apache o Nginx lo publique.
