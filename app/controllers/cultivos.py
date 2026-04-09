from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.config.database import db
from app.models import Cultivo

bp = Blueprint('cultivos', __name__, url_prefix='/cultivos')

@bp.route('/')
@login_required
def listar():
    cultivos = Cultivo.query.all()
    return render_template('cultivos/listar.html', cultivos=cultivos)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nombre_cultivo = request.form.get('nombre_cultivo')
        ciclo_dias = request.form.get('ciclo_dias_aprox')
        
        cultivo = Cultivo(
            nombre_cultivo=nombre_cultivo,
            ciclo_dias_aprox=int(ciclo_dias) if ciclo_dias else None
        )
        db.session.add(cultivo)
        db.session.commit()
        
        flash('Cultivo creado exitosamente.', 'success')
        return redirect(url_for('cultivos.listar'))
    
    return render_template('cultivos/crear.html')

@bp.route('/eliminar/<id>', methods=['POST'])
@login_required
def eliminar(id):
    cultivo = Cultivo.query.get(int(id))
    if cultivo:
        db.session.delete(cultivo)
        db.session.commit()
        flash('Cultivo eliminado exitosamente.', 'success')
    else:
        flash('Cultivo no encontrado.', 'danger')
    return redirect(url_for('cultivos.listar'))
