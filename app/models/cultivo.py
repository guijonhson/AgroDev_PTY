from app.config.database import db

class Cultivo(db.Model):
    __tablename__ = 'cultivo'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_cultivo = db.Column(db.String(100), nullable=False)
    ciclo_dias_aprox = db.Column(db.Integer)
    
    producciones = db.relationship('Produccion', back_populates='cultivo')
    registros = db.relationship('RegistroAgricola', back_populates='cultivo')
    gastos = db.relationship('Gasto', back_populates='cultivo')
