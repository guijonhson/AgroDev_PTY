from app.config.database import db

class Producto(db.Model):
    __tablename__ = 'producto'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    tipo_producto = db.Column(db.String(50), nullable=False)
    
    inventarios = db.relationship('Inventario', back_populates='producto')
    registros = db.relationship('RegistroAgricola', back_populates='producto')
