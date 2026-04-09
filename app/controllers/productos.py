from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.config.database import db
from app.models import Producto

bp = Blueprint('productos', __name__, url_prefix='/productos')

@bp.route('/')
@login_required
def listar():
    productos = Producto.query.all()
    return render_template('productos/listar.html', productos=productos)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nombre_producto = request.form.get('nombre_producto')
        tipo_producto = request.form.get('tipo_producto')
        
        producto = Producto(
            nombre_producto=nombre_producto,
            tipo_producto=tipo_producto
        )
        db.session.add(producto)
        db.session.commit()
        
        flash('Producto creado exitosamente.', 'success')
        return redirect(url_for('productos.listar'))
    
    return render_template('productos/crear.html')

@bp.route('/eliminar/<id>', methods=['POST'])
@login_required
def eliminar(id):
    producto = Producto.query.get(int(id))
    if producto:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente.', 'success')
    else:
        flash('Producto no encontrado.', 'danger')
    return redirect(url_for('productos.listar'))
