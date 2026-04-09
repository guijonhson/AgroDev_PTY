from app.config.database import db
from datetime import datetime

class Suscripcion(db.Model):
    __tablename__ = 'suscripcion'
    
    id = db.Column(db.Integer, primary_key=True)
    id_productor = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=False)
    id_plan = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    estado = db.Column(db.String(20), default='activa')
    
    pagos = db.relationship('Pago', back_populates='suscripcion', lazy=True)
    plan = db.relationship('Plan', back_populates='suscripciones')
