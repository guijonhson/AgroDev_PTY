from app.config.database import db
from datetime import datetime

class Gasto(db.Model):
    __tablename__ = 'gasto'
    
    id = db.Column(db.Integer, primary_key=True)
    id_finca = db.Column(db.Integer, db.ForeignKey('finca.id'), nullable=False)
    id_cultivo = db.Column(db.Integer, db.ForeignKey('cultivo.id'))
    tipo_gasto = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    responsable = db.Column(db.String(100))
    
    cultivo = db.relationship('Cultivo', back_populates='gastos')
    finca = db.relationship('Finca', back_populates='gastos')
