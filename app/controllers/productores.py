from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.productor import Productor
from app.config.database import db

bp = Blueprint('productores', __name__, url_prefix='/productores')

@bp.route('/')
@login_required
def listar():
    if current_user.rol != 'administrador':
        flash('No tiene permisos para acceder.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    productores = Productor.query.all()
    return render_template('productores/listar.html', productores=productores)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if current_user.rol != 'administrador':
        flash('No tiene permisos para acceder.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        
        productor = Productor(nombre=nombre, telefono=telefono, correo=correo)
        db.session.add(productor)
        db.session.commit()
        
        flash('Productor creado exitosamente.', 'success')
        return redirect(url_for('productores.listar'))
    
    return render_template('productores/crear.html')

@bp.route('/ver/<int:id>')
@login_required
def ver(id):
    productor = Productor.query.get_or_404(id)
    return render_template('productores/ver.html', productor=productor)
