# Guía de Deploy - AgroDev en Production

## Preparación del Servidor

### 1. Instalar dependencias del sistema
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install python3 python3-pip python3-venv nginx curl
```

### 2. Clonar/subir el proyecto
```bash
cd /var/www/
git clone <repositorio> agrodev
cd agrodev
```

### 3. Configurar entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con los valores correctos
nano .env
```

### 5. Generar SECRET_KEY segura
```bash
python -c "import secrets; print(secrets.token_hex(24))"
```
Agregar el resultado al `.env` en `SECRET_KEY=`

### 6. Configurar base de datos
```bash
# Mover DB fuera del proyecto (recomendado)
sudo mkdir -p /var/lib/agrodev
sudo mv database/agrodev.db /var/lib/agrodev/
sudo chown www-data:www-data /var/lib/agrodev/agrodev.db

# Actualizar DATABASE_URL en .env:
# DATABASE_URL=sqlite:////var/lib/agrodev/agrodev.db
```

### 7. Inicializar datos demo (opcional)
```bash
python init_demo.py
```

## Configuración de Gunicorn

### 1. Crear servicio systemd
```bash
sudo nano /etc/systemd/system/agrodev.service
```

Contenido:
```ini
[Unit]
Description=AgroDev Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/agrodev
Environment="PATH=/var/www/agrodev/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/var/www/agrodev/venv/bin/gunicorn --workers 2 --bind unix:/var/www/agrodev/agrodev.sock -m 007 run:app

[Install]
WantedBy=multi-user.target
```

### 2. Iniciar servicio
```bash
sudo systemctl daemon-reload
sudo systemctl enable agrodev
sudo systemctl start agrodev
sudo systemctl status agrodev
```

## Configuración de Nginx

### 1. Crear configuración
```bash
sudo nano /etc/nginx/sites-available/agrodev
```

Contenido:
```nginx
server {
    listen 80;
    server_name TU_DOMINIO_O_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/agrodev/agrodev.sock;
    }

    location /static {
        alias /var/www/agrodev/app/static;
    }
}
```

### 2. Habilitar sitio
```bash
sudo ln -s /etc/nginx/sites-available/agrodev /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL con Let's Encrypt (Opcional pero recomendado)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

## Verificación

### Probar que la app responde
```bash
curl http://localhost
curl http://tu-dominio.com
```

### Ver logs
```bash
# App
sudo journalctl -u agrodev -f

# Nginx
sudo tail -f /var/log/nginx/error.log
```

## Comandos útiles

```bash
# Reiniciar app
sudo systemctl restart agrodev

# Ver estado
sudo systemctl status agrodev

# Recargar Nginx
sudo systemctl reload nginx

# Backup de DB
cp /var/lib/agrodev/agrodev.db /var/lib/agrodev/backup_$(date +%Y%m%d).db
```

## Notas Importantes

- SQLite es adecuado para 1-3 usuarios concurrently
- Para más usuarios, migrar a PostgreSQL
- Mantener siempre backup de la base de datos
- El primer usuario registrado se convierte en administrador