from app.config.database import db

class Aplicador(db.Model):
    __tablename__ = 'aplicador'
    
    id = db.Column(db.Integer, primary_key=True)
    id_productor = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    
    registros = db.relationship('RegistroAgricola', back_populates='aplicador', lazy=True)
