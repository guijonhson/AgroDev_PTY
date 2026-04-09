from app.config.database import db
from datetime import datetime

class Pago(db.Model):
    __tablename__ = 'pago'
    
    id = db.Column(db.Integer, primary_key=True)
    id_suscripcion = db.Column(db.Integer, db.ForeignKey('suscripcion.id'), nullable=False)
    id_productor = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    monto = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50), default='Yappy')
    referencia = db.Column(db.String(100))
    comprobante = db.Column(db.String(255))
    estado = db.Column(db.String(20), default='pendiente')
    
    suscripcion = db.relationship('Suscripcion', back_populates='pagos')
    productor = db.relationship('Productor', backref='pagos')
