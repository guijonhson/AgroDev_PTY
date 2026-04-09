from app.config.database import db
from datetime import datetime

class Produccion(db.Model):
    __tablename__ = 'produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    id_parcela = db.Column(db.Integer, db.ForeignKey('parcela.id'), nullable=False)
    id_cultivo = db.Column(db.Integer, db.ForeignKey('cultivo.id'), nullable=False)
    fecha_cosecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Float, nullable=False)
    unidad_medida = db.Column(db.String(20), default='kg')
    precio_venta = db.Column(db.Float, default=0)
    observaciones = db.Column(db.Text)
    
    cultivo = db.relationship('Cultivo', back_populates='producciones')
    parcela = db.relationship('Parcela', back_populates='producciones')
    
    @property
    def ingreso_total(self):
        return self.cantidad * self.precio_venta
