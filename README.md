# Gran Hotel Real S.R.L - Sistema de Gestión

Proyecto desarrollado para la materia de Taller de Sistemas Operativos 2. Este repositorio contiene el código fuente del sistema de gestión de habitaciones, diseñado bajo una arquitectura de capas (Frontend y Backend separados) con base de datos PostgreSQL.

## Estado Actual del Proyecto

Hasta el momento, el proyecto cuenta con:
1. **Base de Datos:** PostgreSQL configurado con la tabla `rooms` e inventario inicial.
2. **Backend (API REST):** Desarrollado en Python usando FastAPI. Estructurado en capas (Rutas, Servicios, Conexión BD) para escalabilidad.
3. **Frontend:** Interfaz web minimalista, asíncrona y responsiva utilizando HTML5, Vanilla JS y Tailwind CSS.

> **Nota sobre Usuarios (Login / Personal):** Actualmente **NO** está contemplado en el alcance del proyecto original (PDF) un sistema de autenticación (Login) para el personal en la aplicación web. El proyecto se enfoca en mostrar el estado de las habitaciones de forma abierta para Recepción. La seguridad de acceso se manejará a nivel de Sistema Operativo mediante Samba y cuotas de red.

## Documentación Detallada

Toda la documentación para implementar, probar y entender este sistema está en la carpeta `/docs`:

* [Guía del Frontend](docs/FRONTEND_GUIDE.md)
* [Guía del Backend y Base de Datos](docs/BACKEND_GUIDE.md)
* [Guía de Configuración del Servidor Linux (Red, Samba, DNS, DHCP)](docs/SERVER_SETUP.md)
* [Consultas SQL para Pruebas](docs/test_queries.sql)
