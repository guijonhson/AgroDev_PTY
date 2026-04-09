"""
Script de Migración: SQLite → MongoDB
AgroDev - Sistema de Gestión Agropecuaria
"""
import os
import sys
import sqlite3
from datetime import datetime

# Conectar a MongoDB
from mongoengine import connect, disconnect
from bson.objectid import ObjectId
from pymongo import MongoClient

# Desconectar cualquier conexión existente
disconnect(alias='default')

# Eliminar base de datos existente
client = MongoClient('localhost', 27017)
client.drop_database('agrodev')
client.close()

# Conectar a MongoDB
connect(
    db='agrodev',
    host='localhost',
    port=27017,
    alias='default'
)

print("Base de datos MongoDB limpia")

# Conectar a SQLite
sqlite_path = os.path.join(os.path.dirname(__file__), 'database', 'agrodev.db')
conn = sqlite3.connect(sqlite_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Diccionarios para mapear IDs old -> new ObjectIds
id_mapping = {
    'productores': {},
    'usuarios': {},
    'planes': {},
    'fincas': {},
    'parcelas': {},
    'cultivos': {},
    'productos': {},
    'aplicadores': {},
    'suscripciones': {},
    'pagos': {},
    'registros_agricolas': {},
    'inventarios': {},
    'gastos': {},
    'producciones': {}
}

def migrate_productores():
    """Migrar productores"""
    print("Migrando productores...")
    cursor.execute("SELECT * FROM productor")
    rows = cursor.fetchall()
    
    from app.models.mongo import Productor
    
    for row in rows:
        old_id = row['id_productor']
        produtor = Productor(
            nombre=row['nombre'],
            telefono=row['telefono'],
            correo=row['correo'],
            fecha_registro=datetime.strptime(row['fecha_creacion'], '%Y-%m-%d') if row['fecha_creacion'] else datetime.utcnow()
        )
        produtor.save()
        id_mapping['productores'][old_id] = str(produtor.id)
        print(f"  - Productor: {produtor.nombre} (old: {old_id} -> new: {produtor.id})")
    
    print(f"  [OK] Migrados {len(rows)} productores")

def migrate_planes():
    """Migrar planes"""
    print("\nMigrando planes...")
    cursor.execute("SELECT * FROM plan")
    rows = cursor.fetchall()
    
    from app.models.mongo import Plan
    
    for row in rows:
        old_id = row['id_plan']
        plan = Plan(
            nombre_plan=row['nombre_plan'],
            precio_mensual=row['precio_mensual'],
            descripcion=row['descripcion']
        )
        plan.save()
        id_mapping['planes'][old_id] = str(plan.id)
        print(f"  - Plan: {plan.nombre_plan}")
    
    print(f"  [OK] Migrados {len(rows)} planes")

def migrate_usuarios():
    """Migrar usuarios"""
    print("\nMigrando usuarios...")
    cursor.execute("SELECT * FROM usuario")
    rows = cursor.fetchall()
    
    from app.models.mongo import Usuario
    
    for row in rows:
        old_id = row['id_usuario']
        id_productor_old = row['id_productor']
        id_productor_new = id_mapping['productores'].get(id_productor_old)
        
        if not id_productor_new:
            print(f"  [!] Usuario {row['nombre_usuario']} sin productor, saltando...")
            continue
        
        from app.models.mongo import Productor
        productor = Productor.objects.get(id=ObjectId(id_productor_new))
        
        usuario = Usuario(
            id_productor=productor,
            nombre_usuario=row['nombre_usuario'],
            correo=row['correo'],
            password_hash=row['password_hash'],
            rol=row['rol'],
            activo=bool(row['activo'])
        )
        usuario.save()
        id_mapping['usuarios'][old_id] = str(usuario.id)
        print(f"  - Usuario: {usuario.nombre_usuario} ({usuario.rol})")
    
    print(f"  [OK] Migrados {len(rows)} usuarios")

def migrate_fincas():
    """Migrar fincas"""
    print("\nMigrando fincas...")
    cursor.execute("SELECT * FROM finca")
    rows = cursor.fetchall()
    
    from app.models.mongo import Finca, Productor
    
    for row in rows:
        old_id = row['id_finca']
        id_productor_old = row['id_productor']
        id_productor_new = id_mapping['productores'].get(id_productor_old)
        
        if not id_productor_new:
            print(f"  [!] Finca {row['nombre_finca']} sin productor, saltando...")
            continue
        
        productor = Productor.objects.get(id=ObjectId(id_productor_new))
        
        finca = Finca(
            id_productor=productor,
            nombre_finca=row['nombre_finca'],
            ubicacion=row['ubicacion'],
            area_total=row['area_total']
        )
        finca.save()
        id_mapping['fincas'][old_id] = str(finca.id)
        print(f"  - Finca: {finca.nombre_finca}")
    
    print(f"  [OK] Migradas {len(rows)} fincas")

def migrate_parcelas():
    """Migrar parcelas"""
    print("\nMigrando parcelas...")
    cursor.execute("SELECT * FROM parcela")
    rows = cursor.fetchall()
    
    from app.models.mongo import Parcela, Finca
    
    for row in rows:
        old_id = row['id_parcela']
        id_finca_old = row['id_finca']
        id_finca_new = id_mapping['fincas'].get(id_finca_old)
        
        if not id_finca_new:
            print(f"  [!] Parcela {row['numero_parcela']} sin finca, saltando...")
            continue
        
        finca = Finca.objects.get(id=ObjectId(id_finca_new))
        
        parcela = Parcela(
            id_finca=finca,
            numero_parcela=row['numero_parcela'],
            area=row['area']
        )
        parcela.save()
        id_mapping['parcelas'][old_id] = str(parcela.id)
        print(f"  - Parcela: {parcela.numero_parcela}")
    
    print(f"  [OK] Migradas {len(rows)} parcelas")

def migrate_cultivos():
    """Migrar cultivos"""
    print("\nMigrando cultivos...")
    cursor.execute("SELECT * FROM cultivo")
    rows = cursor.fetchall()
    
    from app.models.mongo import Cultivo
    
    for row in rows:
        old_id = row['id_cultivo']
        cultivo = Cultivo(
            nombre_cultivo=row['nombre_cultivo'],
            ciclo_dias_aprox=row['ciclo_dias_aprox']
        )
        cultivo.save()
        id_mapping['cultivos'][old_id] = str(cultivo.id)
        print(f"  - Cultivo: {cultivo.nombre_cultivo}")
    
    print(f"  [OK] Migrados {len(rows)} cultivos")

def migrate_productos():
    """Migrar productos"""
    print("\nMigrando productos...")
    cursor.execute("SELECT * FROM producto")
    rows = cursor.fetchall()
    
    from app.models.mongo import Producto
    
    for row in rows:
        old_id = row['id_producto']
        producto = Producto(
            nombre_producto=row['nombre_producto'],
            tipo_producto=row['tipo_producto']
        )
        producto.save()
        id_mapping['productos'][old_id] = str(producto.id)
        print(f"  - Producto: {producto.nombre_producto} ({producto.tipo_producto})")
    
    print(f"  [OK] Migrados {len(rows)} productos")

def migrate_aplicadores():
    """Migrar aplicadores"""
    print("\nMigrando aplicadores...")
    cursor.execute("SELECT * FROM aplicador")
    rows = cursor.fetchall()
    
    from app.models.mongo import Aplicador, Productor
    
    for row in rows:
        old_id = row['id_aplicador']
        id_productor_old = row['id_productor']
        id_productor_new = id_mapping['productores'].get(id_productor_old)
        
        if not id_productor_new:
            print(f"  [!] Aplicador {row['nombre']} sin productor, saltando...")
            continue
        
        productor = Productor.objects.get(id=ObjectId(id_productor_new))
        
        aplicador = Aplicador(
            id_productor=productor,
            nombre=row['nombre'],
            cargo=row['cargo']
        )
        aplicador.save()
        id_mapping['aplicadores'][old_id] = str(aplicador.id)
        print(f"  - Aplicador: {aplicador.nombre}")
    
    print(f"  [OK] Migrados {len(rows)} aplicadores")

def migrate_suscripciones():
    """Migrar suscripciones"""
    print("\nMigrando suscripciones...")
    cursor.execute("SELECT * FROM suscripcion")
    rows = cursor.fetchall()
    
    from app.models.mongo import Suscripcion, Productor, Plan
    
    for row in rows:
        old_id = row['id_suscripcion']
        id_productor_old = row['id_productor']
        id_plan_old = row['id_plan']
        
        id_productor_new = id_mapping['productores'].get(id_productor_old)
        id_plan_new = id_mapping['planes'].get(id_plan_old)
        
        if not id_productor_new or not id_plan_new:
            print(f"  [!] Suscripción sin datos completos, saltando...")
            continue
        
        productor = Productor.objects.get(id=ObjectId(id_productor_new))
        plan = Plan.objects.get(id=ObjectId(id_plan_new))
        
        suscripcion = Suscripcion(
            id_productor=productor,
            id_plan=plan,
            fecha_inicio=datetime.strptime(row['fecha_inicio'], '%Y-%m-%d') if row['fecha_inicio'] else datetime.utcnow(),
            fecha_fin=datetime.strptime(row['fecha_fin'], '%Y-%m-%d') if row['fecha_fin'] else None,
            activa=row['estado'] == 'activa'
        )
        suscripcion.save()
        id_mapping['suscripciones'][old_id] = str(suscripcion.id)
        print(f"  - Suscripción: {suscripcion.id}")
    
    print(f"  [OK] Migradas {len(rows)} suscripciones")

def migrate_pagos():
    """Migrar pagos"""
    print("\nMigrando pagos...")
    cursor.execute("SELECT * FROM pago")
    rows = cursor.fetchall()
    
    from app.models.mongo import Pago, Suscripcion
    
    for row in rows:
        old_id = row['id_pago']
        id_suscripcion_old = row['id_suscripcion']
        id_suscripcion_new = id_mapping['suscripciones'].get(id_suscripcion_old)
        
        if not id_suscripcion_new:
            print(f"  [!] Pago sin suscripción, saltando...")
            continue
        
        suscripcion = Suscripcion.objects.get(id=ObjectId(id_suscripcion_new))
        
        pago = Pago(
            id_suscripcion=suscripcion,
            monto=row['monto'],
            fecha_pago=datetime.strptime(row['fecha_pago'], '%Y-%m-%d') if row['fecha_pago'] else datetime.utcnow(),
            metodo_pago=row['metodo_pago'],
            referencia=row['referencia']
        )
        pago.save()
        id_mapping['pagos'][old_id] = str(pago.id)
        print(f"  - Pago: ${pago.monto}")
    
    print(f"  [OK] Migrados {len(rows)} pagos")

def migrate_registros():
    """Migrar registros agrícolas"""
    print("\nMigrando registros agrícolas...")
    cursor.execute("SELECT * FROM registro_agricola")
    rows = cursor.fetchall()
    
    from app.models.mongo import RegistroAgricola, Parcela, Cultivo, Producto, Aplicador
    
    for row in rows:
        id_parcela_old = row['id_parcela']
        id_cultivo_old = row['id_cultivo']
        id_producto_old = row['id_producto']
        id_aplicador_old = row['id_aplicador']
        
        id_parcela_new = id_mapping['parcelas'].get(id_parcela_old)
        id_cultivo_new = id_mapping['cultivos'].get(id_cultivo_old)
        id_producto_new = id_mapping['productos'].get(id_producto_old)
        id_aplicador_new = id_mapping['aplicadores'].get(id_aplicador_old)
        
        if not all([id_parcela_new, id_cultivo_new, id_producto_new, id_aplicador_new]):
            print(f"  [!] Registro incompleto, saltando...")
            continue
        
        parcela = Parcela.objects.get(id=ObjectId(id_parcela_new))
        cultivo = Cultivo.objects.get(id=ObjectId(id_cultivo_new))
        producto = Producto.objects.get(id=ObjectId(id_producto_new))
        aplicador = Aplicador.objects.get(id=ObjectId(id_aplicador_new))
        
        registro = RegistroAgricola(
            id_parcela=parcela,
            id_cultivo=cultivo,
            id_producto=producto,
            id_aplicador=aplicador,
            fecha=datetime.strptime(row['fecha'], '%Y-%m-%d') if row['fecha'] else datetime.utcnow(),
            tipo_control=row['tipo_control'],
            dosis=str(row['dosis']) if row['dosis'] else None,
            observaciones=row['observaciones']
        )
        registro.save()
        id_mapping['registros_agricolas'][row['id_registro']] = str(registro.id)
        print(f"  - Registro: {registro.fecha.strftime('%Y-%m-%d')}")
    
    print(f"  [OK] Migrados {len(rows)} registros")

def migrate_inventarios():
    """Migrar inventarios"""
    print("\nMigrando inventarios...")
    cursor.execute("SELECT * FROM inventario")
    rows = cursor.fetchall()
    
    from app.models.mongo import Inventario, Producto, Finca
    
    for row in rows:
        id_producto_old = row['id_producto']
        id_finca_old = row['id_finca']
        
        id_producto_new = id_mapping['productos'].get(id_producto_old)
        id_finca_new = id_mapping['fincas'].get(id_finca_old)
        
        if not id_producto_new or not id_finca_new:
            print(f"  [!] Inventario incompleto, saltando...")
            continue
        
        producto = Producto.objects.get(id=ObjectId(id_producto_new))
        finca = Finca.objects.get(id=ObjectId(id_finca_new))
        
        inventario = Inventario(
            id_producto=producto,
            id_finca=finca,
            cantidad=row['cantidad'],
            unidad_medida=row['unidad_medida'],
            stock_minimo=row['stock_minimo'],
            costo_unitario=row['costo_unitario'],
            proveedor=row['proveedor']
        )
        inventario.save()
        id_mapping['inventarios'][row['id_inventario']] = str(inventario.id)
        print(f"  - Inventario: {producto.nombre_producto} ({inventario.cantidad} {inventario.unidad_medida})")
    
    print(f"  [OK] Migrados {len(rows)} inventarios")

def migrate_gastos():
    """Migrar gastos"""
    print("\nMigrando gastos...")
    cursor.execute("SELECT * FROM gasto")
    rows = cursor.fetchall()
    
    from app.models.mongo import Gasto, Finca, Cultivo
    
    for row in rows:
        id_finca_old = row['id_finca']
        id_cultivo_old = row['id_cultivo'] if 'id_cultivo' in row.keys() else None
        
        id_finca_new = id_mapping['fincas'].get(id_finca_old)
        id_cultivo_new = id_mapping['cultivos'].get(id_cultivo_old) if id_cultivo_old else None
        
        if not id_finca_new:
            print(f"  [!] Gasto sin finca, saltando...")
            continue
        
        finca = Finca.objects.get(id=ObjectId(id_finca_new))
        cultivo = Cultivo.objects.get(id=ObjectId(id_cultivo_new)) if id_cultivo_new else None
        
        gasto = Gasto(
            id_finca=finca,
            id_cultivo=cultivo,
            tipo_gasto=row['tipo_gasto'],
            monto=row['monto'],
            descripcion=row['descripcion'],
            fecha=datetime.strptime(row['fecha'], '%Y-%m-%d') if row['fecha'] else datetime.utcnow(),
            responsable=row['responsable']
        )
        gasto.save()
        id_mapping['gastos'][row['id_gasto']] = str(gasto.id)
        print(f"  - Gasto: ${gasto.monto} ({gasto.tipo_gasto})")
    
    print(f"  [OK] Migrados {len(rows)} gastos")

def migrate_producciones():
    """Migrar producciones"""
    print("\nMigrando producciones...")
    cursor.execute("SELECT * FROM produccion")
    rows = cursor.fetchall()
    
    from app.models.mongo import Produccion, Parcela, Cultivo
    
    for row in rows:
        id_parcela_old = row['id_parcela']
        id_cultivo_old = row['id_cultivo']
        
        id_parcela_new = id_mapping['parcelas'].get(id_parcela_old)
        id_cultivo_new = id_mapping['cultivos'].get(id_cultivo_old)
        
        if not id_parcela_new or not id_cultivo_new:
            print(f"  [!] Producción incompleta, saltando...")
            continue
        
        parcela = Parcela.objects.get(id=ObjectId(id_parcela_new))
        cultivo = Cultivo.objects.get(id=ObjectId(id_cultivo_new))
        
        produccion = Produccion(
            id_parcela=parcela,
            id_cultivo=cultivo,
            fecha_cosecha=datetime.strptime(row['fecha_cosecha'], '%Y-%m-%d') if row['fecha_cosecha'] else datetime.utcnow(),
            cantidad=row['cantidad'],
            unidad_medida=row['unidad_medida'],
            precio_venta=row['precio_venta'],
            observaciones=row['observaciones']
        )
        produccion.save()
        id_mapping['producciones'][row['id_produccion']] = str(produccion.id)
        print(f"  - Producción: {produccion.cantidad} {produccion.unidad_medida}")
    
    print(f"  [OK] Migradas {len(rows)} producciones")


def main():
    print("=" * 60)
    print("MIGRACION SQLite -> MongoDB")
    print("AgroDev - Sistema de Gestion Agropecuaria")
    print("=" * 60)
    
    # Migrar en orden
    migrate_productores()
    migrate_planes()
    migrate_usuarios()
    migrate_fincas()
    migrate_parcelas()
    migrate_cultivos()
    migrate_productos()
    migrate_aplicadores()
    migrate_suscripciones()
    migrate_pagos()
    migrate_registros()
    migrate_inventarios()
    migrate_gastos()
    migrate_producciones()
    
    print("\n" + "=" * 60)
    print("MIGRACION COMPLETADA!")
    print("=" * 60)
    
    # Cerrar conexión SQLite
    conn.close()


if __name__ == '__main__':
    main()
