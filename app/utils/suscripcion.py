from app.config.database import db
from app.models import Finca, Parcela, Inventario, Gasto, RegistroAgricola, Suscripcion, Plan
from app.models.usuario import Usuario
from datetime import datetime


def obtener_suscripcion_activa(id_productor):
    """Obtiene la suscripcion activa del productor"""
    suscripcion = Suscripcion.query.filter_by(
        id_productor=id_productor,
        estado='activa'
    ).first()
    return suscripcion


def esta_suscripcion_activa(id_productor):
    """Verifica si la suscripcion esta activa y no ha vencido"""
    suscripcion = obtener_suscripcion_activa(id_productor)
    
    if not suscripcion:
        return False
    
    # Verificar si la suscripcion ha vencido
    if suscripcion.fecha_fin:
        if suscripcion.fecha_fin < datetime.now().date():
            # Marcar como vencida
            suscripcion.estado = 'vencida'
            db.session.commit()
            return False
    
    return True


def es_admin(id_productor):
    """Verifica si el productor es admin"""
    admin_usuarios = Usuario.query.filter_by(
        id_productor=id_productor,
        rol='administrador'
    ).count()
    return admin_usuarios > 0


def obtener_plan(id_plan):
    """Obtiene un plan por su ID"""
    return Plan.query.get(id_plan)


def verificar_limite(id_productor, tipo_recurso):
    """
    Verifica si el productor puede crear mas recursos segun su plan.
    Retorna (puede_crear, mensaje)
    
    IMPORTANTE: Los administradores tienen acceso ilimitado a todo.
    """
    # Administrador siempre tiene acceso ilimitado
    if es_admin(id_productor):
        return True, None
    
    # Verificar si la suscripcion esta activa
    if not esta_suscripcion_activa(id_productor):
        return False, "Tu suscripcion ha vencido. Renueva tu plan para continuar."
    
    suscripcion = obtener_suscripcion_activa(id_productor)
    
    if not suscripcion:
        return False, "No tienes una suscripcion activa. Elige un plan para continuar."
    
    plan = suscripcion.plan
    if not plan:
        return False, "Error: Plan no encontrado. Contacta al administrador."
    
    # Obtener atributos del limite segun tipo de recurso
    limite_attr_map = {
        'finca': 'limite_fincas',
        'parcela': 'limite_parcelas',
        'inventario': 'limite_productos',
        'usuario': 'limite_usuarios',
        'gasto': 'limite_productos',  # Usar productos como referencia
    }
    
    if tipo_recurso not in limite_attr_map:
        return True, None
    
    limite_attr = limite_attr_map[tipo_recurso]
    limite = getattr(plan, limite_attr, 0)
    
    # None significa ilimitado
    if limite is None:
        return True, None
    
    # Contar recursos actuales
    count = 0
    
    if tipo_recurso == 'finca':
        count = Finca.query.filter_by(id_productor=id_productor).count()
    
    elif tipo_recurso == 'parcela':
        fincas = Finca.query.filter_by(id_productor=id_productor).all()
        fincas_ids = [f.id for f in fincas]
        count = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).count() if fincas_ids else 0
    
    elif tipo_recurso == 'inventario':
        fincas = Finca.query.filter_by(id_productor=id_productor).all()
        fincas_ids = [f.id for f in fincas]
        count = Inventario.query.filter(Inventario.id_finca.in_(fincas_ids)).count() if fincas_ids else 0
    
    elif tipo_recurso == 'usuario':
        count = Usuario.query.filter_by(id_productor=id_productor).count()
    
    elif tipo_recurso == 'gasto':
        fincas = Finca.query.filter_by(id_productor=id_productor).all()
        fincas_ids = [f.id for f in fincas]
        count = Gasto.query.filter(Gasto.id_finca.in_(fincas_ids)).count() if fincas_ids else 0
    
    # Comparar con limite
    if count >= limite:
        # Mensajes UX amigables
        mensajes = {
            'finca': f"Tu plan {plan.nombre_plan} permite solo {limite} {'finca' if limite == 1 else 'fincas'}. Actualiza tu plan para seguir crescendo.",
            'parcela': f"Tu plan {plan.nombre_plan} permite solo {limite} {'parcela' if limite == 1 else 'parcelas'}. Actualiza tu plan para seguir crescendo.",
            'inventario': f"Tu plan {plan.nombre_plan} permite solo {limite} productos en inventario. Actualiza tu plan para seguir crescendo.",
            'usuario': f"Tu plan {plan.nombre_plan} permite solo {limite} {'usuario' if limite == 1 else 'usuarios'}. Actualiza tu plan para mas usuarios.",
            'gasto': f"Tu plan {plan.nombre_plan} permite solo {limite} {'gasto' if limite == 1 else 'gastos'}. Actualiza tu plan para seguir crescendo."
        }
        return False, mensajes.get(tipo_recurso, f"Limite alcanzado ({limite})")
    
    return True, None


def puede_usar_funcionalidad(id_productor, funcionalidad):
    """
    Verifica si el productor puede usar una funcionalidad especifica segun su plan.
    Los administradores siempre tienen acceso a todo.
    """
    # Administrador siempre tiene acceso
    if es_admin(id_productor):
        return True
    
    suscripcion = obtener_suscripcion_activa(id_productor)
    
    if not suscripcion:
        return False
    
    plan = suscripcion.plan
    
    # Mapeo de funcionalidades a atributos del plan
    func_map = {
        'reportes_avanzados': 'reportes_avanzados',
        'exportar_datos': 'exportar_datos'
    }
    
    if funcionalidad in func_map:
        attr = func_map[funcionalidad]
        return getattr(plan, attr, False)
    
    return True


def puede_acceder_ruta(id_productor, ruta):
    """Verifica si puede acceder a una ruta especifica segun su plan."""
    if es_admin(id_productor):
        return True
    
    # Rutas que requieren PRO
    rutas_pro = ['/reportes/avanzados', '/exportar']
    
    if ruta in rutas_pro:
        return puede_usar_funcionalidad(id_productor, 'reportes_avanzados')
    
    return True


def obtener_limites_plan(id_productor):
    """Retorna los limites del plan actual del productor"""
    suscripcion = obtener_suscripcion_activa(id_productor)
    if not suscripcion:
        return None
    
    plan = suscripcion.plan
    return {
        'limite_fincas': plan.limite_fincas,
        'limite_usuarios': plan.limite_usuarios,
        'limite_parcelas': plan.limite_parcelas,
        'limite_productos': plan.limite_productos,
        'reportes_avanzados': plan.reportes_avanzados,
        'exportar_datos': plan.exportar_datos,
        'nombre_plan': plan.nombre_plan,
        'precio': plan.precio_mensual
    }


def contar_recursos(id_productor):
    """Cuenta los recursos actuales del productor"""
    fincas = Finca.query.filter_by(id_productor=id_productor).all()
    fincas_ids = [f.id for f in fincas]
    
    # Contar melalui parcelas
    parcelas = Parcela.query.filter(Parcela.id_finca.in_(fincas_ids)).all() if fincas_ids else []
    parcelas_ids = [p.id for p in parcelas]
    
    count_inventario = Inventario.query.filter(Inventario.id_finca.in_(fincas_ids)).count() if fincas_ids else 0
    count_gastos = Gasto.query.filter(Gasto.id_finca.in_(fincas_ids)).count() if fincas_ids else 0
    count_registros = RegistroAgricola.query.filter(RegistroAgricola.id_parcela.in_(parcelas_ids)).count() if parcelas_ids else 0
    usuarios = Usuario.query.filter_by(id_productor=id_productor).count()
    
    return {
        'fincas': len(fincas),
        'parcelas': len(parcelas),
        'inventario': count_inventario,
        'usuarios': usuarios,
        'gastos': count_gastos,
        'registros': count_registros
    }


def asignar_plan(id_productor, nombre_plan):
    """Asigna un plan al productor"""
    plan = Plan.query.filter_by(nombre_plan=nombre_plan).first()
    
    if not plan:
        return None, f"Plan {nombre_plan} no encontrado"
    
    from datetime import timedelta
    
    # Eliminar suscripcion anterior
    Suscripcion.query.filter_by(id_productor=id_productor).delete()
    
    # Crear nueva suscripcion
    suscripcion = Suscripcion(
        id_productor=id_productor,
        id_plan=plan.id,
        fecha_inicio=datetime.now().date(),
        fecha_fin=datetime.now().date() + timedelta(days=30),
        estado='activa'
    )
    db.session.add(suscripcion)
    db.session.commit()
    
    return suscripcion, None


def formatear_limite(valor):
    """Formatea el limite para mostrar en frontend"""
    if valor is None:
        return "Ilimitado"
    return str(valor)
