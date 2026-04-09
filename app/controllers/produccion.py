from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.produccion import Produccion
from app.models.cultivo import Cultivo
from app.models.parcela import Parcela
from app.models.finca import Finca
from app.config.database import db
from datetime import datetime

bp = Blueprint('produccion', __name__, url_prefix='/produccion')

@bp.route('/')
@login_required
def listar():
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    parcelas_ids = [p.id for p in parcelas]
    producciones = Produccion.query.filter(Produccion.id_parcela.in_(parcelas_ids)).order_by(Produccion.fecha_cosecha.desc()).all()
    return render_template('produccion/listar.html', producciones=producciones)

@bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    cultivos = Cultivo.query.all()
    
    if request.method == 'POST':
        id_cultivo = request.form.get('id_cultivo')
        id_parcela = request.form.get('id_parcela')
        fecha_cosecha = request.form.get('fecha_cosecha')
        cantidad = request.form.get('cantidad')
        unidad_medida = request.form.get('unidad_medida')
        precio_venta = request.form.get('precio_venta')
        observaciones = request.form.get('observaciones')
        
        produccion = Produccion(
            id_cultivo=int(id_cultivo),
            id_parcela=int(id_parcela),
            fecha_cosecha=datetime.strptime(fecha_cosecha, '%Y-%m-%d').date() if fecha_cosecha else datetime.utcnow().date(),
            cantidad=float(cantidad) if cantidad else 0,
            unidad_medida=unidad_medida or 'kg',
            precio_venta=float(precio_venta) if precio_venta else 0,
            observaciones=observaciones
        )
        db.session.add(produccion)
        db.session.commit()
        
        flash('Producción registrada exitosamente.', 'success')
        return redirect(url_for('produccion.listar'))
    
    return render_template('produccion/crear.html', parcelas=parcelas, cultivos=cultivos)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    produccion = Produccion.query.get_or_404(id)
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    cultivos = Cultivo.query.all()
    
    if request.method == 'POST':
        produccion.id_cultivo = int(request.form.get('id_cultivo'))
        produccion.id_parcela = int(request.form.get('id_parcela'))
        produccion.fecha_cosecha = datetime.strptime(request.form.get('fecha_cosecha'), '%Y-%m-%d').date() if request.form.get('fecha_cosecha') else datetime.utcnow().date()
        produccion.cantidad = float(request.form.get('cantidad')) if request.form.get('cantidad') else 0
        produccion.unidad_medida = request.form.get('unidad_medida') or 'kg'
        produccion.precio_venta = float(request.form.get('precio_venta')) if request.form.get('precio_venta') else 0
        produccion.observaciones = request.form.get('observaciones')
        db.session.commit()
        
        flash('Producción actualizada exitosamente.', 'success')
        return redirect(url_for('produccion.listar'))
    
    return render_template('produccion/editar.html', produccion=produccion, parcelas=parcelas, cultivos=cultivos)

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    produccion = Produccion.query.get_or_404(id)
    db.session.delete(produccion)
    db.session.commit()
    flash('Registro de producción eliminado.', 'success')
    return redirect(url_for('produccion.listar'))

@bp.route('/resumen')
@login_required
def resumen():
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    parcelas_ids = [p.id for p in parcelas]
    producciones = Produccion.query.filter(Produccion.id_parcela.in_(parcelas_ids)).all()
    
    total_cosechas = len(producciones)
    total_cantidad = sum(float(p.cantidad or 0) for p in producciones)
    total_ingreso = sum(p.ingreso_total for p in producciones)
    
    resumen_cultivos = {}
    for p in producciones:
        cultivo_nombre = p.cultivo.nombre_cultivo if p.cultivo else 'Sin cultivo'
        if cultivo_nombre not in resumen_cultivos:
            resumen_cultivos[cultivo_nombre] = {
                'cultivo': cultivo_nombre,
                'cosechas': 0,
                'cantidad': 0,
                'unidad': p.unidad_medida,
                'ingreso': 0,
                'precio_promedio': 0
            }
        resumen_cultivos[cultivo_nombre]['cosechas'] += 1
        resumen_cultivos[cultivo_nombre]['cantidad'] += float(p.cantidad or 0)
        resumen_cultivos[cultivo_nombre]['ingreso'] += p.ingreso_total
    
    for item in resumen_cultivos.values():
        if item['cantidad'] > 0:
            item['precio_promedio'] = item['ingreso'] / item['cantidad']
    
    ultimas_cosechas = Produccion.query.filter(Produccion.id_parcela.in_(parcelas_ids)).order_by(Produccion.fecha_cosecha.desc()).limit(5).all()
    
    return render_template('produccion/resumen.html',
                         producciones=producciones,
                         total_cosechas=total_cosechas,
                         total_cantidad=total_cantidad,
                         total_ingreso=total_ingreso,
                         resumen_cultivos=list(resumen_cultivos.values()),
                         ultimas_cosechas=ultimas_cosechas)
