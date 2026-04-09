from app.config.database import db
from datetime import datetime

class RegistroAgricola(db.Model):
    __tablename__ = 'registro_agricola'
    
    id = db.Column(db.Integer, primary_key=True)
    id_parcela = db.Column(db.Integer, db.ForeignKey('parcela.id'), nullable=False)
    id_cultivo = db.Column(db.Integer, db.ForeignKey('cultivo.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    id_aplicador = db.Column(db.Integer, db.ForeignKey('aplicador.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tipo_control = db.Column(db.String(50), nullable=False)
    dosis = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    
    cultivo = db.relationship('Cultivo', back_populates='registros')
    producto = db.relationship('Producto', back_populates='registros')
    parcela = db.relationship('Parcela', back_populates='registros')
    aplicador = db.relationship('Aplicador', back_populates='registros')
