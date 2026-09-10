# Gran Hotel Real S.R.L - Gestión Centralizada de Servicios en Linux

Este proyecto ha sido desarrollado para la materia de **Taller de Sistemas Operativos 2**. Consiste en la administración integral de un servidor Linux para centralizar los servicios de red de un hotel simulado, integrando además una aplicación web para la gestión de habitaciones.

## 🎯 Propósito y Objetivo del Proyecto

**¿Por qué se está diseñando de este modo?**
El propósito fundamental de este proyecto NO es simplemente crear una página web, sino **demostrar empíricamente las capacidades de administración, control de recursos e infraestructura que ofrece un Sistema Operativo Linux**.

En un entorno corporativo real, el software depende de una infraestructura subyacente sólida. Este diseño busca simular un ecosistema empresarial donde un **único Servidor Linux** actúa como el cerebro central que:
1.  Asigna direcciones IP a las computadoras del personal (DHCP).
2.  Traduce los nombres de dominio para facilitar el acceso interno (DNS).
3.  Protege y comparte documentos confidenciales entre áreas (Samba).
4.  Aloja la aplicación web de gestión, controlando de forma estricta cuánta memoria y procesador puede consumir (Systemd y cgroups).

## 📈 Avance Actual del Proyecto (Lo que ya tenemos)

Hasta este momento, hemos completado exitosamente la **Fase de Software y Lógica**:
- [x] **Base de Datos:** Implementación de PostgreSQL con el diseño de tablas (ERD) e inserción del inventario inicial de las habitaciones.
- [x] **Backend (API REST):** Construcción del motor en Python (FastAPI) estructurado bajo Arquitectura de N-Capas (Rutas, Servicios, Conexión BD) libre de acentos y totalmente técnico.
- [x] **Frontend:** Maquetación de la interfaz gráfica minimalista y responsiva (UI/UX con Tailwind CSS) para que Recepción consulte la disponibilidad en tiempo real.
- [x] **Documentación Técnica:** Creación de las guías de Frontend, Backend y consultas SQL de prueba.

## 🚧 Puntos Faltantes y Plan de Acción (Fase de Servidor)

Para concluir el proyecto al 100% y prepararlo para la defensa, falta implementar la **Fase de Infraestructura Linux**, la cual es el núcleo de evaluación de la materia. 

Los hitos pendientes son:
- [ ] **Red Base:** Despliegue de la máquina virtual (Ubuntu/Debian) fijando la IP estática en `192.168.10.2`.
- [ ] **Servicios de Red (Telecomunicaciones):** Instalación de `isc-dhcp-server` para las terminales y `bind9` (DNS) para resolver el dominio interno `hotelreal.local`.
- [ ] **Servicio de Archivos (Samba):** Creación de una carpeta compartida de solo lectura (Manuales de Recepción) y otra privada con clave (Reportes de Administración).
- [ ] **Control y Límites (Seguridad Operativa):**
  - **UFW (Firewall):** Cierre de puertos innecesarios.
  - **Systemd:** Creación del servicio para el Backend, limitando su consumo de RAM a un máximo de 200MB.
  - **Traffic Control (tc):** Priorización de paquetes DNS/Web por encima de la transferencia de archivos Samba.
- [ ] **Pruebas de Contingencia y Seguridad:**
  - Simular conflicto por una IP Duplicada en la red y rastrearlo en logs.
  - Provocar la caída del servicio web (`kill -9`) y demostrar cómo Systemd lo auto-recupera instantáneamente.
  - Dañar intencionalmente una entrada de zona en BIND9 y documentar su corrección.
- [ ] **Documentación Final:** Anexar capturas de pantalla de la terminal demostrando que las contingencias fueron resueltas exitosamente.

> **Nota sobre las Guías:** En la carpeta `docs/SERVER_SETUP.md` encontrarás el manual detallado de configuración con los comandos exactos que se utilizarán para lograr estos puntos faltantes.
