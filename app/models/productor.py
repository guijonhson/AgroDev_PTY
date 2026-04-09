from app.config.database import db
from datetime import datetime

class Productor(db.Model):
    __tablename__ = 'productor'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    fecha_creacion = db.Column(db.Date, default=datetime.utcnow)
    
    fincas = db.relationship('Finca', backref='productor', lazy=True, cascade='all, delete-orphan')
    usuarios = db.relationship('Usuario', backref='productor', lazy=True, cascade='all, delete-orphan')
    aplicadores = db.relationship('Aplicador', backref='productor', lazy=True, cascade='all, delete-orphan')
    suscripciones = db.relationship('Suscripcion', backref='productor', lazy=True)
    
    def to_dict(self):
        return {
            'id_productor': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'correo': self.correo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
