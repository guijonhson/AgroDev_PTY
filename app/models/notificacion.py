from app.config.database import db
from datetime import datetime

class Notificacion(db.Model):
    __tablename__ = 'notificacion'
    
    id = db.Column(db.Integer, primary_key=True)
    id_productor = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=True)
    mensaje = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), default='info')
    leido = db.Column(db.Boolean, default=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    productor = db.relationship('Productor', backref='notificaciones')
