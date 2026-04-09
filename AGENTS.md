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
├── DEPLOY.md               # Guía producción
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
pytest tests/test_archivo.py     # Un archivo
pytest tests/test.py::test_fn    # Una función
pytest -v                        # Verbose
pytest -k "patron"               # Por nombre
```

### Base de Datos
```bash
del database\agrodev.db
venv\Scripts\python -c "from app import create_app; create_app()"
sqlite3 database/agrodev.db "ALTER TABLE tabla ADD COLUMN col TIPO;"
venv\Scripts\python init_demo.py
```

## Convenciones de Código

### Imports
```python
from app.config.database import db
from app.models import Usuario, Productor, Finca
from app.utils.suscripcion import verificar_limite
```

### Nombres
- Clases: PascalCase (`Productor`, `Usuario`)
- Funciones/variables: snake_case
- Blueprints: minúsculas (`fincas`, `auth`)

### SQLAlchemy
```python
# Crear
p = Productor(nombre="Juan")
db.session.add(p)
db.session.commit()

# Consultar
u = Usuario.query.filter_by(correo=correo).first()
fincas = Finca.query.filter_by(id_productor=id_productor).all()

# Primary key: usar 'id' (NO id_productor, id_finca)
id = db.Column(db.Integer, primary_key=True)

# Relaciones: back_populates (NO backref)
class Finca(db.Model):
    parcelas = db.relationship('Parcela', back_populates='finca')
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

### Errores
- Usar `flash()` para mensajes
- Usar `get_or_404()` para consultas obligatorias

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

### Planes
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

# Admin siempre tiene acceso ilimitado
es_admin(id_productor)  # True/False
```

### Notas Importantes
- **Ilimitado**: Usar `None` en la base de datos (NO usar -1)
- **Admin**: Siempre tiene acceso ilimitado
- **Verificar expiración**: `esta_suscripcion_activa(id_productor)`

## Tecnologías

- Flask 3.0.0, SQLAlchemy, SQLite
- Flask-Login 0.6.3, Flask-Bcrypt 1.0.1
- Bootstrap 5.3.0, Bootstrap Icons 1.10.0
- Gunicorn (producción)

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

- SQLite, NO MongoDB
- Primer usuario = administrador
- Usar `current_user.id_productor` al filtrar
- LSP errores en SQLAlchemy son falsos positivos
- DB se crea automáticamente
- Nuevos campos: usar ALTER TABLE
- Frontend: navbar con offcanvas (Bootstrap)
- Suscripciones: límites en None = ilimitado
- Admin siempre tiene acceso ilimitado

## Producción

```bash
SECRET_KEY=generar-hex
FLASK_ENV=production
FLASK_DEBUG=False
gunicorn -w 2 -b 0.0.0.0:8000 run:app
```
