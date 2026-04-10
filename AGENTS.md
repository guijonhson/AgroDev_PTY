# AGENTS.md - AgroDev Sistema de Gestión Agropecuaria

## Descripción General

AgroDev es un sistema SaaS de gestión agrícola basado en Flask con SQLite. Soporta multiusuario, control de roles (administrador/cliente), gestión de fincas/parcelas, cultivos, suscripciones y notificaciones.

## Estructura del Proyecto

```
agrodev/
├── app/
│   ├── __init__.py          # Fábrica Flask
│   ├── config/database.py   # SQLAlchemy
│   ├── models/             # Modelos DB
│   ├── controllers/         # Blueprints
│   ├── templates/           # Jinja2
│   └── static/css/         # Responsive
├── config.py               # Config (dev/prod)
├── database/agrodev.db      # SQLite
├── run.py                  # Ejecutor
├── init_demo.py            # Datos demo
├── requirements.txt        # Dependencias
└── .env.example           # Variables entorno
```

## Comandos

### Instalar y Ejecutar
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
venv\Scripts\python run.py
```

### Pruebas con pytest
```bash
pytest                          # Todas
pytest tests/test_archivo.py    # Un archivo
pytest tests/test.py::test_fn   # Una función específica
pytest -v                       # Verbose
pytest -k "patron"              # Por nombre
pytest --cov=app               # Con coverage
pytest --cov-report=html        # Reporte HTML
```

### Linting y Type Checking
```bash
ruff check .                   # Lint todo el proyecto
ruff check app/models/         # Lint directorio específico
ruff check --fix .             # Auto-corregir
mypy app/                      # Type checking
```

### Base de Datos
```bash
del database\agrodev.db
venv\Scripts\python -c "from app import create_app; create_app()"
sqlite3 database/agrodev.db "ALTER TABLE tabla ADD COLUMN col TIPO;"
venv\Scripts\python init_demo.py
```

## Convenciones de Código

### Imports (orden estándar)
```python
# 1. stdlib
import os
import re
from datetime import datetime

# 2. third-party
from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_bcrypt import Bcrypt

# 3. local
from app.config.database import db
from app.models import Usuario, Productor, Finca
from app.utils.suscripcion import verificar_limite
```

### Nomenclatura
- **Clases**: PascalCase (`Productor`, `Usuario`, `FincaMapper`)
- **Funciones/variables**: snake_case (`nombre_finca`, `get_user_by_email`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_LOGIN_ATTEMPTS`)
- **Blueprints**: minúsculas (`fincas`, `auth`, `inventario`)
- **Tablas/Columnas**: snake_case (`nombre_finca`, `id_productor`)

### SQLAlchemy
```python
# Primary key: usar 'id' (NO id_productor, id_finca)
id = db.Column(db.Integer, primary_key=True)

# Relaciones: back_populates (NO backref)
class Finca(db.Model):
    __tablename__ = 'fincas'
    parcelas = db.relationship('Parcela', back_populates='finca')

# Consultas
u = Usuario.query.filter_by(correo=correo).first()
fincas = Finca.query.filter_by(id_productor=id_productor).all()
```

### Flask-Login
```python
class Usuario(db.Model):
    @property
    def is_authenticated(self): return True
    @property
    def is_active(self): return self.activo if self.activo is not None else True
    @property
    def is_anonymous(self): return False
    def get_id(self): return str(self.id)
```

### Manejo de Errores
- Usar `flash()` para mensajes al usuario
- Usar `get_or_404()` para consultas obligatorias
- Try/except solo donde sea necesario, no abusar
- Registrar errores con `app.logger.error()`

## HTML/Jinja2

```html
<a href="{{ url_for('fincas.editar', id=finca.id) }}">Editar</a>
<td>{{ parcela.finca.nombre_finca }}</td>
<!-- Grid: col-12 col-sm-6 col-lg-3 -->
<!-- Tablas: table-responsive o table-stack -->
```

## Seguridad

```python
# Contraseñas
usuario.set_password(password)
usuario.check_password(password)

# Roles
@login_required
def dashboard():
    if current_user.rol != 'administrador':
        flash('No tiene permisos.', 'danger')
        return redirect(url_for('dashboard.index'))

# Filtrar por usuario
fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
```

## Sistema de Suscripciones

| Plan | Fincas | Usuarios | Parcelas | Productos | Precio |
|------|--------|----------|----------|-----------|--------|
| FREE | 1 | 1 | 5 | 50 | $0 |
| BÁSICO | 3 | 2 | 15 | 200 | $10 |
| PRO | 10 | 5 | 50 | 1000 | $25 |
| EMPRESARIAL | Ilimitado | Ilimitado | Ilimitado | Ilimitado | $50 |

### Uso
```python
from app.utils.suscripcion import verificar_limite, es_admin

# Verificar límite
puede, mensaje = verificar_limite(current_user.id_productor, 'finca')
if not puede:
    flash(mensaje, 'warning')
    return redirect(url_for('suscripciones.upgrade'))
```

## Errores a Evitar

```python
# NO usar MongoDB
Usuario.objects(correo=correo).first()  # INCORRECTO
Usuario.query.filter_by(correo=correo).first()  # CORRECTO

# NO primary keys personalizadas
id_productor = db.Column(db.Integer, primary_key=True)  # INCORRECTO
id = db.Column(db.Integer, primary_key=True)  # CORRECTO

# NO usar -1 para ilimitado, usar None
limite_fincas = -1  # INCORRECTO
limite_fincas = None  # CORRECTO
```

## Notas para Agentes

- **SQLite, NO MongoDB** - Usar SQLAlchemy
- Primer usuario = administrador
- Usar `current_user.id_productor` al filtrar datos
- LSP errores en SQLAlchemy son falsos positivos
- DB se crea automáticamente con `db.create_all()`
- Nuevos campos: usar ALTER TABLE
- Frontend: navbar con offcanvas (Bootstrap)
- Admin siempre tiene acceso ilimitado

## Producción

```bash
SECRET_KEY=generar-hex
FLASK_ENV=production
FLASK_DEBUG=False
gunicorn -w 2 -b 0.0.0.0:8000 run:app
```