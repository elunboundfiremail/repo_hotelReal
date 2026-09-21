# Guía Definitiva - Proyecto Hotel Real (Avance 50%)


---

## ⚙️ PRE-REQUISITO EN VMWARE (Inmunidad al cambio de WiFi)
Para que tu IP estática funcione y el servidor tenga internet a la vez, necesitamos 2 tarjetas de red virtuales. Haz esto con la máquina apagada:

1. Abre **VMware** -> Clic derecho en tu máquina virtual -> **Settings** (Configuraciones).
2. Selecciona **Network Adapter** (Adaptador de Red). A la derecha, asegúrate de que esté marcado **NAT** (Esto le dará internet para descargar cosas).
3. Haz clic abajo en el botón **Add...** (Agregar) -> Selecciona **Network Adapter** -> **Finish**.
4. Selecciona el nuevo adaptador que acabas de crear y a la derecha marca **Host-only: A private network shared with the host** (Esto crea la red privada para tu IP Estática).
5. Haz clic en **OK** y enciende la máquina virtual.

---

## 💻 Paso 1: Configuración de IP Estática (Netplan)
Fijaremos la IP en el adaptador Host-Only.

1. Ejecuta `ip a`. Verás dos tarjetas (por ejemplo `ens33` que tiene internet, y `ens37` o `ens36` que no tiene IP). Asumiremos que la segunda es `ens37`.
2. Edita la configuración de red:
   ```bash
   sudo nano /etc/netplan/00-installer-config.yaml
   ```
3. Modifica para que quede así (respeta espacios, sin tabs). Añade tu segunda tarjeta (`ens37`):
   ```yaml
   network:
     version: 2
     ethernets:
       ens33:
         dhcp4: true
       ens37:
         dhcp4: no
         addresses: [192.168.19.10/24]
   ```
4. Aplica los cambios:
   ```bash
   sudo netplan apply
   ```

---

## 👥 Paso 2: Usuarios, Grupos y Permisos (Laboratorio)
Crearemos el personal y su carpeta confidencial.

1. Crear el grupo y los usuarios con contraseña:
   ```bash
   sudo groupadd hotel_staff
   sudo useradd -m -s /bin/bash recepcion
   sudo passwd recepcion
   ```
   *(⚠️ Nota: Linux te exigirá una contraseña segura. Usa algo como `Recepcion_2026!` que tenga mayúscula, números y símbolos para que te la acepte).*

   ```bash
   sudo useradd -m -s /bin/bash gerencia
   sudo passwd gerencia
   ```
   *(⚠️ Usa algo como `Gerencia_2026!`)*

   ```bash
   sudo usermod -aG hotel_staff recepcion
   sudo usermod -aG hotel_staff gerencia
   ```
2. Crear carpeta de reportes confidenciales y asignar permisos (770):
   ```bash
   sudo mkdir -p /var/hotel_reportes
   sudo chown root:hotel_staff /var/hotel_reportes
   sudo chmod 770 /var/hotel_reportes
   ```

---

## 🛡️ Paso 3: Firewall (UFW) y SSH Seguro
1. Configurar reglas básicas:
   ```bash
   sudo apt update && sudo apt install ufw -y
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # Web Frontend
   sudo ufw allow 8000/tcp  # Web Backend (FastAPI)
   sudo ufw allow 53/tcp    # DNS
   sudo ufw allow 53/udp    # DNS
   sudo ufw --force enable
   ```

---

## 🗄️ Paso 4: Motor PostgreSQL, Administrador y Soporte
1. Instalar y asegurar que inicie siempre (24/7):
   ```bash
   sudo apt install postgresql postgresql-contrib -y
   sudo systemctl enable postgresql
   sudo systemctl start postgresql
   ```
2. Crear la Carpeta de Soporte/Backups (Para las copias de seguridad):
   ```bash
   sudo mkdir -p /var/soporte_hotel
   sudo chown postgres:postgres /var/soporte_hotel
   sudo chmod 700 /var/soporte_hotel
   ```
3. Cambiar la contraseña del administrador de Base de Datos y crear el usuario del hotel:
   ```bash
   # Entrar a Postgres
   sudo -u postgres psql
   ```
   *Dentro de Postgres (la terminal cambiará a `postgres=#`), ejecuta:*
   ```sql
   ALTER USER postgres PASSWORD 'admin123';
   CREATE USER admin_db_hotel WITH PASSWORD 'hotel123';
   CREATE DATABASE db_hotelreal OWNER admin_db_hotel;
   \q
   ```

---

## 🌐 Paso 5: Servidor DNS (BIND9)
1. Instalar el servicio:
   ```bash
   sudo apt install bind9 bind9utils -y
   sudo systemctl enable bind9
   ```
2. Configurar zona en `sudo nano /etc/bind/named.conf.local`:
   ```text
   zone "hotelreal.com.bo" {
       type master;
       file "/etc/bind/db.hotelreal";
   };
   ```
3. Archivo de Base de Datos en `sudo nano /etc/bind/db.hotelreal`:
   ```text
   $TTL    604800
   @       IN      SOA     ns.hotelreal.com.bo. admin.hotelreal.com.bo. (
                         2         ; Serial
                    604800         ; Refresh
                     86400         ; Retry
                   2419200         ; Expire
                    604800 )       ; Negative Cache TTL
   ;
   @       IN      NS      ns.hotelreal.com.bo.
   @       IN      A       192.168.19.10
   ns      IN      A       192.168.19.10
   www     IN      A       192.168.19.10
   ```
4. Reiniciar:
   ```bash
   sudo systemctl restart named
   ```

---

## 🚀 Paso 6: Inicialización de la Base de Datos y Despliegue Web
1. Cargar las tablas del Hotel a PostgreSQL:
   ```bash
   sudo -u postgres psql -d db_hotelreal -f /home/user/proyecto_hotel/database/schema.sql
   ```
2. Dar permisos al usuario del hotel para que pueda leer las tablas (Corrección de privilegios):
   ```bash
   sudo -u postgres psql -d db_hotelreal -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_db_hotel;"
   sudo -u postgres psql -d db_hotelreal -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_db_hotel;"
   ```
3. Levantar el Backend (FastAPI):
   ```bash
   cd /home/user/proyecto_hotel/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 &
   ```
4. Levantar el Frontend (Web):
   ```bash
   cd /home/user/proyecto_hotel/frontend
   sudo python3 -m http.server 80 &
   ```

---

## 🚨 Paso 7: Pruebas de Contingencia y Casos Especiales
Todo buen administrador de sistemas debe demostrar que su servidor resiste ataques y errores. Haz estas pruebas para cerrar tu informe con broche de oro:

**Prueba 1: Intento de Violación de Seguridad (Permisos)**
Vamos a demostrar que el `chmod 770` funciona simulando que un usuario "X" (que no es del hotel) intenta ver los reportes confidenciales.
```bash
# Cambiamos temporalmente al usuario "games" (un usuario del sistema que no es del grupo hotel_staff)
sudo -u games ls -la /var/hotel_reportes
```

**Prueba 2: Eficacia del Firewall (Puertos bloqueados)**
Nuestro UFW solo tiene abiertos el 22 (SSH), 80 (Web) y 53 (DNS). Vamos a probar si el Firewall bloquea un intento de conexión a un puerto cerrado (por ejemplo, el 8080).
```bash
# Intentamos forzar una conexión de red local a un puerto cerrado
curl -v telnet://192.168.19.10:8080
```

**Prueba 3: Resolución Local vs IP (DNS)**
Verificar que la máquina sabe quién es `hotelreal.com.bo` gracias a BIND9.
```bash
nslookup hotelreal.com.bo
```
