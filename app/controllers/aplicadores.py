from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.config.database import db
from app.models import Aplicador

bp = Blueprint('aplicadores', __name__, url_prefix='/aplicadores')

@bp.route('/')
@login_required
def listar():
    aplicadores = Aplicador.query.filter_by(id_productor=current_user.id_productor).all()
    return render_template('aplicadores/listar.html', aplicadores=aplicadores)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cargo = request.form.get('cargo')
        
        aplicador = Aplicador(
            id_productor=current_user.id_productor,
            nombre=nombre,
            cargo=cargo
        )
        db.session.add(aplicador)
        db.session.commit()
        
        flash('Aplicador creado exitosamente.', 'success')
        return redirect(url_for('aplicadores.listar'))
    
    return render_template('aplicadores/crear.html')

@bp.route('/eliminar/<id>', methods=['POST'])
@login_required
def eliminar(id):
    aplicador = Aplicador.query.get(int(id))
    if not aplicador:
        flash('Aplicador no encontrado.', 'danger')
        return redirect(url_for('aplicadores.listar'))
    
    if aplicador.id_productor != current_user.id_productor:
        flash('No tiene permisos para acceder.', 'danger')
        return redirect(url_for('aplicadores.listar'))
    
    db.session.delete(aplicador)
    db.session.commit()
    flash('Aplicador eliminado exitosamente.', 'success')
    return redirect(url_for('aplicadores.listar'))
