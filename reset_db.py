"""
Script de Reset de Base de Datos - AgroDev

Este script limpia toda la base de datos manteniendo unicamente el usuario administrador.

Uso:
    python reset_db.py
"""
from app import create_app
from app.config.database import db
from app.models import (
    Finca, Parcela, Inventario, Gasto, RegistroAgricola,
    Produccion, Pago, Suscripcion, Notificacion,
    Productor, Usuario, Cultivo, Producto, Aplicador, Plan
)
from datetime import datetime, timedelta


def reset_database():
    """Reinicia la base de datos conservando solo el admin"""
    
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print(" RESETEANDO BASE DE DATOS - AGRODEV ")
        print("="*60 + "\n")
        
        # 1. IDENTIFICAR ADMIN
        print("[*] Buscando administrador...")
        admin = Usuario.query.filter_by(rol='administrador').first()
        
        if not admin:
            print("ERROR: No se encontro usuario administrador")
            return
        
        id_productor_admin = admin.id_productor
        print(f"[OK] Admin encontrado: {admin.correo}")
        print(f"     ID Usuario: {admin.id}")
        print(f"     ID Productor: {id_productor_admin}\n")
        
        # 2. ELIMINAR DATOS RELACIONADOS (orden por dependencias)
        print("[*] Eliminando datos...")
        
        # Registros agricolas (depende de parcela)
        reg_count = RegistroAgricola.query.delete()
        print(f"    - Registros agricolas: {reg_count}")
        
        # Producciones (depende de parcela)
        prod_count = Produccion.query.delete()
        print(f"    - Producciones: {prod_count}")
        
        # Parcelas (depende de finca)
        parc_count = Parcela.query.delete()
        print(f"    - Parcelas: {parc_count}")
        
        # Inventarios (depende de finca)
        inv_count = Inventario.query.delete()
        print(f"    - Inventarios: {inv_count}")
        
        # Gastos (depende de finca)
        gast_count = Gasto.query.delete()
        print(f"    - Gastos: {gast_count}")
        
        # Fincas
        fing_count = Finca.query.delete()
        print(f"    - Fincas: {fing_count}")
        
        # Pagos
        pag_count = Pago.query.delete()
        print(f"    - Pagos: {pag_count}")
        
        # Suscripciones
        susc_count = Suscripcion.query.delete()
        print(f"    - Suscripciones: {susc_count}")
        
        # Notificaciones
        noti_count = Notificacion.query.delete()
        print(f"    - Notificaciones: {noti_count}")
        
        # Aplicadores
        apli_count = Aplicador.query.delete()
        print(f"    - Aplicadores: {apli_count}")
        
        # Eliminar otros usuarios (no admin)
        otros_usuarios = Usuario.query.filter(Usuario.id != admin.id).delete()
        print(f"    - Otros usuarios eliminados: {otros_usuarios}")
        
        # Eliminar otros productores (no el del admin)
        otros_productores = Productor.query.filter(Productor.id != id_productor_admin).delete()
        print(f"    - Otros productores eliminados: {otros_productores}")
        
        db.session.commit()
        print("\n[OK] Datos eliminados correctamente\n")
        
        # 3. CREAR FINCA INICIAL PARA ADMIN
        print("[*] Creando finca inicial...")
        financa = Finca(
            nombre_finca="Mi Finca Principal",
            ubicacion="Por definir",
            area_total=1.0,
            id_productor=id_productor_admin
        )
        db.session.add(financa)
        db.session.commit()
        print(f"    - Finca creada: {financa.nombre_finca} (ID: {financa.id})\n")
        
        # 4. VERIFICAR/OBTENER PLAN PRO
        print("[*] Verificando plan PRO...")
        plan_pro = Plan.query.filter_by(nombre_plan='PRO').first()
        
        if not plan_pro:
            print("    [W] Plan PRO no existe, creando...")
            plan_pro = Plan(
                nombre_plan='PRO',
                precio_mensual=25.0,
                descripcion='Plan profesional completo',
                limite_fincas=-1,
                limite_usuarios=-1,
                limite_parcelas=-1,
                limite_registros=-1,
                limite_inventario=-1,
                limite_gastos=-1,
                reportes_avanzados=True,
                exportar_datos=True,
                activo=True
            )
            db.session.add(plan_pro)
            db.session.commit()
            print("    [OK] Plan PRO creado")
        else:
            print(f"    [OK] Plan PRO encontrado: {plan_pro.nombre_plan}")
        
        # 5. ASIGNAR SUSCRIPCION PRO ILIMITADA
        print("[*] Asignando suscripcion PRO...")
        
        # Eliminar suscripciones anteriores del admin
        Suscripcion.query.filter_by(id_productor=id_productor_admin).delete()
        
        suscripcion = Suscripcion(
            id_productor=id_productor_admin,
            id_plan=plan_pro.id,
            fecha_inicio=datetime.now().date(),
            fecha_fin=datetime.now().date() + timedelta(days=3650),  # 10 anos
            estado='activa'
        )
        db.session.add(suscripcion)
        db.session.commit()
        print(f"    [OK] Suscripcion PRO activa hasta: {suscripcion.fecha_fin}")
        
        # 6. VALIDACION FINAL
        print("\n" + "="*60)
        print(" RESETE COMPLETADO ")
        print("="*60)
        
        # Verificaciones
        total_usuarios = Usuario.query.count()
        total_fincas = Finca.query.count()
        total_productores = Productor.query.count()
        
        print(f"\n VALIDACION FINAL:")
        print(f"    Usuarios totales: {total_usuarios} (debe ser 1)")
        print(f"    Fincas totales: {total_fincas} (debe ser 1)")
        print(f"    Productores totales: {total_productores} (debe ser 1)")
        
        # Verificar suscripcion
        suscrit = Suscripcion.query.filter_by(id_productor=id_productor_admin, estado='activa').first()
        if suscrit:
            print(f"    Suscripcion: {suscrit.plan.nombre_plan} - {suscrit.estado}")
        
        print(f"\n El sistema ha sido reseteado correctamente!")
        print(f" El administrador {admin.correo} tiene acceso ILIMITADO")
        print(f" Puede iniciar sesion normalmente.\n")


if __name__ == '__main__':
    reset_database()
