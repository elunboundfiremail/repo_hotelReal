# Guía de Configuración del Servidor Linux (Infraestructura)

Esta guía explica los pasos manuales para configurar los servicios de red requeridos en el Servidor Ubuntu/Debian para el Gran Hotel Real. Estos servicios correrán en paralelo a nuestra aplicación web.

## 1. Asignación de IP Estática
El servidor debe tener la IP `192.168.10.2`.
- Edita el archivo de Netplan: `sudo nano /etc/netplan/00-installer-config.yaml`
- Configura la interfaz (ej. `ens33`) con IP fija, sin DHCP, y aplica con `sudo netplan apply`.

## 2. Servidor DHCP (isc-dhcp-server)
Encargado de dar IPs (192.168.10.10 al 20) a las terminales de Recepción y Administración.
- **Instalación:** `sudo apt install isc-dhcp-server`
- **Configuración:** Edita `/etc/dhcp/dhcpd.conf`:
  ```text
  subnet 192.168.10.0 netmask 255.255.255.0 {
      range 192.168.10.10 192.168.10.20;
      option domain-name-servers 192.168.10.2;
      option domain-name "hotelreal.local";
  }
  ```
- **Reinicio:** `sudo systemctl restart isc-dhcp-server`

## 3. Servidor DNS (bind9)
Resuelve el nombre `hotelreal.local` a la IP del servidor.
- **Instalación:** `sudo apt install bind9 bind9utils bind9-doc`
- **Zonas:** En `/etc/bind/named.conf.local` declara la zona `hotelreal.local`.
- **Archivo de Zona:** Crea `/etc/bind/db.hotelreal.local` apuntando el registro `A` de `web` y `@` a `192.168.10.2`.
- **Reinicio:** `sudo systemctl restart bind9`

## 4. Servidor de Archivos Compartidos (Samba)
Crea las carpetas para Recepción (Solo lectura) y Administración (Protegida).
- **Instalación:** `sudo apt install samba`
- **Carpetas:** `sudo mkdir -p /srv/samba/recepcion` y `/srv/samba/administracion`
- **Usuarios:** Crea usuarios de sistema y asígnales password en samba (`sudo smbpasswd -a admin_user`).
- **Configuración (`/etc/samba/smb.conf`):**
  ```ini
  [Recepcion]
     path = /srv/samba/recepcion
     read only = yes
     guest ok = yes
  [Administracion]
     path = /srv/samba/administracion
     valid users = admin_user
     read only = no
  ```

## 5. Control de Recursos y Firewall
- **Systemd:** Para limitar la RAM del backend, edita o crea el servicio systemd (`/etc/systemd/system/hotelbackend.service`) y añade `MemoryMax=200M`.
- **UFW (Firewall):** 
  ```bash
  sudo ufw allow 22/tcp  # SSH
  sudo ufw allow 53      # DNS
  sudo ufw allow 67/udp  # DHCP
  sudo ufw allow 80/tcp  # Web Nginx
  sudo ufw allow 8080/tcp # Backend FastAPI
  sudo ufw allow Samba
  sudo ufw enable
  ```

> **Correlación con el Proyecto:** El Frontend y Backend que programamos vivirán dentro de este mismo servidor. Nginx (puerto 80) mostrará el Frontend, y el Backend correrá en el 8080. El DNS permitirá que las recepcionistas entren a `http://web.hotelreal.local` en vez de usar la IP.
