from app.config.database import db
from datetime import datetime

class Inventario(db.Model):
    __tablename__ = 'inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    id_finca = db.Column(db.Integer, db.ForeignKey('finca.id'), nullable=False)
    cantidad = db.Column(db.Float, default=0)
    unidad_medida = db.Column(db.String(20), default='kg')
    stock_minimo = db.Column(db.Float, default=0)
    costo_unitario = db.Column(db.Float, default=0)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    proveedor = db.Column(db.String(100))
    
    producto = db.relationship('Producto', back_populates='inventarios')
    finca = db.relationship('Finca', back_populates='inventarios')
    
    @property
    def valor_total(self):
        return (self.cantidad or 0) * (self.costo_unitario or 0)
    
    @property
    def bajo_stock(self):
        return (self.cantidad or 0) <= (self.stock_minimo or 0)
