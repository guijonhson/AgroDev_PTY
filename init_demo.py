"""
Script para crear datos de DEMO en AgroDev
Ejecutar: python init_demo.py
"""
from app import create_app
from app.config.database import db
from app.models import Productor, Usuario, Finca, Parcela, Cultivo, Gasto, Produccion, Suscripcion, Plan
from datetime import datetime, timedelta

def crear_datos_demo():
    app = create_app()
    
    with app.app_context():
        print("Creando datos de DEMO...")
        
        # Verificar si ya hay datos
        if Productor.query.count() > 0:
            print("Ya existen datos en la base de datos. No se crearán datos demo.")
            return
        
        # 1. Crear Productor Demo
        productor = Productor(
            nombre="Demo AgroDev",
            telefono="6000-0000",
            correo="demo@agrodev.com"
        )
        db.session.add(productor)
        db.session.commit()
        print(f"✓ Productor creado: {productor.nombre}")
        
        # 2. Crear Usuario Demo (Cliente)
        plan_free = Plan.query.filter_by(nombre_plan='FREE').first()
        
        usuario_demo = Usuario(
            nombre_usuario="Demo User",
            correo="demo@agrodev.com",
            id_productor=productor.id,
            rol="cliente",
            activo=True
        )
        usuario_demo.set_password("demo123")
        db.session.add(usuario_demo)
        db.session.commit()
        print(f"✓ Usuario demo creado: demo@agrodev.com / demo123")
        
        # 3. Crear Suscripción FREE
        suscripcion = Suscripcion(
            id_productor=productor.id,
            id_plan=plan_free.id,
            fecha_inicio=datetime.now().date(),
            fecha_fin=datetime.now().date() + timedelta(days=30),
            estado="activa"
        )
        db.session.add(suscripcion)
        db.session.commit()
        print(f"✓ Suscripción FREE creada")
        
        # 4. Crear Fincas Demo
        fincas_data = [
            {"nombre": "Finca Santa Rosa", "ubicacion": "Chepo, Panamá", "area": 25.5},
            {"nombre": "Finca El Progreso", "ubicacion": "Capira, Panamá", "area": 15.0},
        ]
        
        for f in fincas_data:
            financa = Finca(
                nombre_finca=f["nombre"],
                ubicacion=f["ubicacion"],
                area_total=f["area"],
                id_productor=productor.id
            )
            db.session.add(finca)
        
        db.session.commit()
        print(f"✓ {len(fincas_data)} fincas creadas")
        
        # Obtener las fincas creadas
        fincas = Finca.query.filter_by(id_productor=productor.id).all()
        
        # 5. Crear Parcelas Demo
        parcelas_data = [
            {"finca": fincas[0], "numero": 1, "area": 5.0},
            {"finca": fincas[0], "numero": 2, "area": 8.5},
            {"finca": fincas[1], "numero": 1, "area": 7.0},
        ]
        
        for p in parcelas_data:
            parcela = Parcela(
                numero_parcela=p["numero"],
                area_parcela=p["area"],
                id_finca=p["finca"].id,
                id_productor=productor.id
            )
            db.session.add(parcela)
        
        db.session.commit()
        print(f"✓ {len(parcelas_data)} parcelas creadas")
        
        # Obtener parcelas para cultivos y actividades
        parcelas = Parcela.query.filter_by(id_productor=productor.id).all()
        
        # 6. Obtener cultivos
        maiz = Cultivo.query.filter_by(nombre_cultivo='Maíz').first()
        frijol = Cultivo.query.filter_by(nombre_cultivo='Frijol').first()
        
        # 7. Crear Gastos Demo
        gastos_data = [
            {"descripcion": "Fertilizante urea", "monto": 150.00, "categoria": "Fertilizantes"},
            {"descripcion": "Glifosato 5L", "monto": 85.50, "category": "Herbicidas"},
            {"descripcion": "Mano de obra cosecha", "monto": 200.00, "categoria": "Labor"},
            {"descripcion": "Gasolina tractor", "monto": 75.00, "categoria": "Combustible"},
        ]
        
        for g in gastos_data:
            gasto = Gasto(
                descripcion=g["descripcion"],
                monto=g["monto"],
                categoria=g.get("categoria", "Otros"),
                id_finca=fincas[0].id,
                id_productor=productor.id,
                fecha_gasto=datetime.now().date() - timedelta(days=5)
            )
            db.session.add(gasto)
        
        db.session.commit()
        print(f"✓ {len(gastos_data)} gastos creados")
        
        # 8. Crear Producciones Demo
        produccion_data = [
            {"id_parcela": parcelas[0].id, "cultivo": maiz, "cantidad": 50, "precio": 0.45},
            {"id_parcela": parcelas[1].id, "cultivo": frijol, "cantidad": 25, "precio": 1.20},
        ]
        
        for prod in produccion_data:
            produccion = Produccion(
                cantidad_producida=prod["cantidad"],
                unidad_medida="qq",
                precio_unitario=prod["precio"],
                id_parcela=prod["id_parcela"],
                id_cultivo=prod["cultivo"].id,
                id_productor=productor.id,
                fecha_cosecha=datetime.now().date() - timedelta(days=10)
            )
            produccion.calcular_ingreso()
            db.session.add(produccion)
        
        db.session.commit()
        print(f"✓ {len(produccion_data)} producciones creadas")
        
        print("\n" + "="*50)
        print("DATOS DE DEMO CREADOS EXITOSAMENTE")
        print("="*50)
        print("\nCredenciales de acceso:")
        print("  Email: demo@agrodev.com")
        print("  Contraseña: demo123")
        print("\nRol: Cliente (puede ver todas las opciones excepto admin)")

if __name__ == '__main__':
    crear_datos_demo()