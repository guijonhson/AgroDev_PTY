from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models.registro_agricola import RegistroAgricola
from app.models.cultivo import Cultivo
from app.models.producto import Producto
from app.models.parcela import Parcela
from app.models.finca import Finca

bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@bp.route('/')
@login_required
def index():
    return render_template('reportes/index.html')

@bp.route('/buscar', methods=['POST'])
@login_required
def buscar():
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    id_cultivo = request.form.get('id_cultivo')
    id_producto = request.form.get('id_producto')
    id_parcela = request.form.get('id_parcela')
    
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    parcelas_ids = [p.id for p in parcelas]
    
    query = RegistroAgricola.query.filter(RegistroAgricola.id_parcela.in_(parcelas_ids))
    
    if id_cultivo:
        query = query.filter(RegistroAgricola.id_cultivo == int(id_cultivo))
    if id_producto:
        query = query.filter(RegistroAgricola.id_producto == int(id_producto))
    if id_parcela:
        query = query.filter(RegistroAgricola.id_parcela == int(id_parcela))
    
    registros = query.order_by(RegistroAgricola.fecha.desc()).all()
    
    cultivos = Cultivo.query.all()
    productos = Producto.query.all()
    parcelas_all = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    
    return render_template('reportes/resultados.html', 
                          registros=registros,
                          cultivos=cultivos, 
                          productos=productos,
                          parcelas=parcelas_all)

@bp.route('/resumen')
@login_required
def resumen():
    fincas = Finca.query.filter_by(id_productor=current_user.id_productor).all()
    fincas_ids = [f.id for f in fincas]
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all()
    parcelas_ids = [p.id for p in parcelas]
    
    total_registros = RegistroAgricola.query.filter(RegistroAgricola.id_parcela.in_(parcelas_ids)).count()
    
    registros_por_cultivo = []
    for cultivo in Cultivo.query.all():
        count = RegistroAgricola.query.filter(
            RegistroAgricola.id_parcela.in_(parcelas_ids),
            RegistroAgricola.id_cultivo == cultivo.id
        ).count()
        if count > 0:
            registros_por_cultivo.append((cultivo.nombre_cultivo, count))
    
    registros_por_producto = []
    for producto in Producto.query.all():
        count = RegistroAgricola.query.filter(
            RegistroAgricola.id_parcela.in_(parcelas_ids),
            RegistroAgricola.id_producto == producto.id
        ).count()
        if count > 0:
            registros_por_producto.append((producto.nombre_producto, producto.tipo_producto, count))
    
    return render_template('reportes/resumen.html',
                          total_registros=total_registros,
                          registros_por_cultivo=registros_por_cultivo,
                          registros_por_producto=registros_por_producto)
