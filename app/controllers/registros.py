from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.config.database import db
from app.models import RegistroAgricola, Cultivo, Producto, Parcela, Aplicador, Finca
from datetime import datetime

bp = Blueprint('registros', __name__, url_prefix='/registros')

@bp.route('/')
@login_required
def listar():
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    parcelas_ids = [p.id for p in parcelas]
    registros = RegistroAgricola.query.filter(RegistroAgricola.id_parcela.in_(parcelas_ids)).order_by(RegistroAgricola.fecha.desc()).all()
    return render_template('registros/listar.html', registros=registros)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    cultivos = Cultivo.query.all()
    productos = Producto.query.all()
    aplicadores = Aplicador.query.filter_by(id_productor=current_user.id_productor).all()
    
    if request.method == 'POST':
        fecha = datetime.strptime(request.form.get('fecha'), '%Y-%m-%d')
        id_cultivo = request.form.get('id_cultivo')
        id_producto = request.form.get('id_producto')
        tipo_control = request.form.get('tipo_control')
        dosis = request.form.get('dosis')
        id_parcela = request.form.get('id_parcela')
        id_aplicador = request.form.get('id_aplicador')
        observaciones = request.form.get('observaciones')
        
        registro = RegistroAgricola(
            fecha=fecha,
            id_cultivo=int(id_cultivo),
            id_producto=int(id_producto),
            tipo_control=tipo_control,
            dosis=dosis,
            id_parcela=int(id_parcela),
            id_aplicador=int(id_aplicador),
            observaciones=observaciones
        )
        db.session.add(registro)
        db.session.commit()
        
        flash('Registro agricola creado exitosamente.', 'success')
        return redirect(url_for('registros.listar'))
    
    return render_template('registros/crear.html', 
                          fincas=fincas, parcelas=parcelas, 
                          cultivos=cultivos, productos=productos, 
                          aplicadores=aplicadores)

@bp.route('/ver/<id>')
@login_required
def ver(id):
    registro = RegistroAgricola.query.get(int(id))
    return render_template('registros/ver.html', registro=registro)

@bp.route('/eliminar/<id>', methods=['POST'])
@login_required
def eliminar(id):
    registro = RegistroAgricola.query.get(int(id))
    if registro:
        db.session.delete(registro)
        db.session.commit()
        flash('Registro eliminado exitosamente.', 'success')
    else:
        flash('Registro no encontrado.', 'danger')
    return redirect(url_for('registros.listar'))
