from app.config.database import db


class Plan(db.Model):
    __tablename__ = 'plan'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_plan = db.Column(db.String(50), nullable=False, unique=True)
    precio_mensual = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    
    # Limites de recursos (None = ilimitado)
    limite_fincas = db.Column(db.Integer, default=1)
    limite_usuarios = db.Column(db.Integer, default=1)
    limite_parcelas = db.Column(db.Integer, default=5)
    limite_productos = db.Column(db.Integer, default=50)
    
    # Funcionalidades booleanas
    reportes_avanzados = db.Column(db.Boolean, default=False)
    exportar_datos = db.Column(db.Boolean, default=False)
    
    suscripciones = db.relationship('Suscripcion', back_populates='plan')


def init_planes():
    """Inicializa los planes en la base de datos"""
    from app.models import Plan
    
    # Verificar si ya existen planes
    if Plan.query.count() > 0:
        return
    
    planes_data = [
        {
            'nombre_plan': 'FREE',
            'precio_mensual': 0.0,
            'descripcion': 'Plan gratuito para empezar con tu negocio agricola',
            'limite_fincas': 1,
            'limite_usuarios': 1,
            'limite_parcelas': 5,
            'limite_productos': 50,
            'reportes_avanzados': False,
            'exportar_datos': False,
            'activo': True
        },
        {
            'nombre_plan': 'BÁSICO',
            'precio_mensual': 10.0,
            'descripcion': 'Plan ideal para pequenas empresas agricolas',
            'limite_fincas': 3,
            'limite_usuarios': 2,
            'limite_parcelas': 15,
            'limite_productos': 200,
            'reportes_avanzados': True,
            'exportar_datos': False,
            'activo': True
        },
        {
            'nombre_plan': 'PRO',
            'precio_mensual': 25.0,
            'descripcion': 'Plan profesional para empresas en crecimiento',
            'limite_fincas': 10,
            'limite_usuarios': 5,
            'limite_parcelas': 50,
            'limite_productos': 1000,
            'reportes_avanzados': True,
            'exportar_datos': True,
            'activo': True
        },
        {
            'nombre_plan': 'EMPRESARIAL',
            'precio_mensual': 50.0,
            'descripcion': 'Plan ilimitado para grandes empresas',
            'limite_fincas': None,  # Ilimitado
            'limite_usuarios': None,  # Ilimitado
            'limite_parcelas': None,  # Ilimitado
            'limite_productos': None,  # Ilimitado
            'reportes_avanzados': True,
            'exportar_datos': True,
            'activo': True
        }
    ]
    
    for plan_data in planes_data:
        plan = Plan(**plan_data)
        db.session.add(plan)
    
    db.session.commit()
