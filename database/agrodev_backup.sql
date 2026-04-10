PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE productor (
	id INTEGER NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	telefono VARCHAR(20), 
	correo VARCHAR(100), 
	fecha_creacion DATE, 
	PRIMARY KEY (id)
);
INSERT INTO productor VALUES(1,'Guillermo Jonhson','6944-2874','guijonhson22@gmail.com','2026-03-25');
CREATE TABLE cultivo (
	id INTEGER NOT NULL, 
	nombre_cultivo VARCHAR(100) NOT NULL, 
	ciclo_dias_aprox INTEGER, 
	PRIMARY KEY (id)
);
INSERT INTO cultivo VALUES(1,'Maíz',120);
INSERT INTO cultivo VALUES(2,'Frijol',90);
INSERT INTO cultivo VALUES(3,'Arroz',150);
INSERT INTO cultivo VALUES(4,'Caña de azúcar',365);
INSERT INTO cultivo VALUES(5,'Papa',120);
INSERT INTO cultivo VALUES(6,'Tomate',90);
INSERT INTO cultivo VALUES(7,'Plátano',300);
INSERT INTO cultivo VALUES(8,'Yuca',180);
INSERT INTO cultivo VALUES(9,'pacas',30);
CREATE TABLE producto (
	id INTEGER NOT NULL, 
	nombre_producto VARCHAR(100) NOT NULL, 
	tipo_producto VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO producto VALUES(1,'Glifosato','herbicida');
INSERT INTO producto VALUES(2,'2,4-D','herbicida');
INSERT INTO producto VALUES(3,'Atrazina','herbicida');
INSERT INTO producto VALUES(4,'Mancozeb','fungicida');
INSERT INTO producto VALUES(5,'Carbendazim','fungicida');
INSERT INTO producto VALUES(6,'Urea','fertilizante');
INSERT INTO producto VALUES(7,'NPK 10-30-10','fertilizante');
INSERT INTO producto VALUES(8,'Fosfato diamónico','fertilizante');
INSERT INTO producto VALUES(9,'Cypermethrin','insecticida');
INSERT INTO producto VALUES(10,'Chlorpyrifos','insecticida');
INSERT INTO producto VALUES(11,'Daconate ','herbicida');
INSERT INTO producto VALUES(12,'prueba','herbicida');
CREATE TABLE IF NOT EXISTS "plan" (
	id INTEGER NOT NULL, 
	nombre_plan VARCHAR(50) NOT NULL, 
	precio_mensual FLOAT NOT NULL, 
	descripcion TEXT, 
	activo BOOLEAN, limite_fincas INTEGER DEFAULT 1, limite_usuarios INTEGER DEFAULT 1, limite_parcelas INTEGER DEFAULT 5, limite_inventario INTEGER DEFAULT 50, limite_registros INTEGER DEFAULT 10, limite_gastos INTEGER DEFAULT 10, reportes_avanzados INTEGER DEFAULT 0, exportar_datos INTEGER DEFAULT 0, limite_productos INTEGER DEFAULT 50, 
	PRIMARY KEY (id)
);
INSERT INTO "plan" VALUES(1,'FREE',0.0,'Plan gratuito para empezar con tu negocio agricola',1,1,1,5,50,10,10,0,0,50);
INSERT INTO "plan" VALUES(2,'BÁSICO',10.0,'Plan ideal para pequenas empresas agricolas',1,3,2,15,50,10,10,1,0,200);
INSERT INTO "plan" VALUES(3,'PRO',25.0,'Plan profesional para empresas en crecimiento',1,10,5,50,50,10,10,1,1,1000);
INSERT INTO "plan" VALUES(4,'EMPRESARIAL',50.0,'Plan ilimitado para grandes empresas',1,NULL,NULL,NULL,50,10,10,1,1,NULL);
CREATE TABLE usuario (
	id INTEGER NOT NULL, 
	id_productor INTEGER NOT NULL, 
	nombre_usuario VARCHAR(50) NOT NULL, 
	correo VARCHAR(100) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	rol VARCHAR(20) NOT NULL, 
	activo BOOLEAN, ultimo_acceso DATETIME, fecha_registro DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_productor) REFERENCES productor (id)
);
INSERT INTO usuario VALUES(1,1,'Guillermo Jonhson','guijonhson22@gmail.com','$2b$12$ADrHUZ96XwsZBYocCyNbcOcLQAAkLzcJT/CC/Vfvqh5ft9g9loBxS','administrador',1,'2026-04-09 16:13:53.899809',NULL);
CREATE TABLE finca (
	id INTEGER NOT NULL, 
	id_productor INTEGER NOT NULL, 
	nombre_finca VARCHAR(100) NOT NULL, 
	ubicacion VARCHAR(200), 
	area_total FLOAT, 
	fecha_registro DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_productor) REFERENCES productor (id)
);
INSERT INTO finca VALUES(1,1,'Mi Finca Principal','Por definir',1.0,'2026-04-09 19:50:20.434239');
INSERT INTO finca VALUES(2,1,'pronto','bugaba',5.0,'2026-04-09 20:10:52.921082');
CREATE TABLE aplicador (
	id INTEGER NOT NULL, 
	id_productor INTEGER NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	cargo VARCHAR(50), 
	telefono VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_productor) REFERENCES productor (id)
);
CREATE TABLE suscripcion (
	id INTEGER NOT NULL, 
	id_productor INTEGER NOT NULL, 
	id_plan INTEGER NOT NULL, 
	fecha_inicio DATE NOT NULL, 
	fecha_fin DATE, 
	estado VARCHAR(20), 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_productor) REFERENCES productor (id), 
	FOREIGN KEY(id_plan) REFERENCES "plan" (id)
);
INSERT INTO suscripcion VALUES(1,1,4,'2026-04-09','2027-04-09','activa');
INSERT INTO suscripcion VALUES(2,2,1,'2026-04-09',NULL,'activa');
CREATE TABLE parcela (
	id INTEGER NOT NULL, 
	id_finca INTEGER NOT NULL, 
	numero_parcela VARCHAR(50) NOT NULL, 
	area FLOAT, 
	cultivo_actual VARCHAR(100), 
	fecha_registro DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_finca) REFERENCES finca (id)
);
INSERT INTO parcela VALUES(1,1,'01',1.0,NULL,'2026-04-09 20:11:16.073843');
CREATE TABLE pago (
	id INTEGER NOT NULL, 
	id_suscripcion INTEGER NOT NULL, 
	fecha_pago DATE NOT NULL, 
	monto FLOAT NOT NULL, 
	metodo_pago VARCHAR(50), 
	referencia VARCHAR(100), 
	estado VARCHAR(20), id_productor INTEGER, comprobante VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_suscripcion) REFERENCES suscripcion (id)
);
CREATE TABLE inventario (
	id INTEGER NOT NULL, 
	id_producto INTEGER NOT NULL, 
	id_finca INTEGER NOT NULL, 
	cantidad FLOAT, 
	unidad_medida VARCHAR(20), 
	stock_minimo FLOAT, 
	costo_unitario FLOAT, 
	fecha_ingreso DATETIME, 
	proveedor VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_producto) REFERENCES producto (id), 
	FOREIGN KEY(id_finca) REFERENCES finca (id)
);
CREATE TABLE gasto (
	id INTEGER NOT NULL, 
	id_finca INTEGER NOT NULL, 
	id_cultivo INTEGER, 
	tipo_gasto VARCHAR(50) NOT NULL, 
	monto FLOAT NOT NULL, 
	descripcion TEXT, 
	fecha DATE NOT NULL, 
	responsable VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_finca) REFERENCES finca (id), 
	FOREIGN KEY(id_cultivo) REFERENCES cultivo (id)
);
CREATE TABLE registro_agricola (
	id INTEGER NOT NULL, 
	id_parcela INTEGER NOT NULL, 
	id_cultivo INTEGER NOT NULL, 
	id_producto INTEGER NOT NULL, 
	id_aplicador INTEGER NOT NULL, 
	fecha DATE NOT NULL, 
	tipo_control VARCHAR(50) NOT NULL, 
	dosis VARCHAR(50), 
	observaciones TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_parcela) REFERENCES parcela (id), 
	FOREIGN KEY(id_cultivo) REFERENCES cultivo (id), 
	FOREIGN KEY(id_producto) REFERENCES producto (id), 
	FOREIGN KEY(id_aplicador) REFERENCES aplicador (id)
);
CREATE TABLE produccion (
	id INTEGER NOT NULL, 
	id_parcela INTEGER NOT NULL, 
	id_cultivo INTEGER NOT NULL, 
	fecha_cosecha DATE NOT NULL, 
	cantidad FLOAT NOT NULL, 
	unidad_medida VARCHAR(20), 
	precio_venta FLOAT, 
	observaciones TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_parcela) REFERENCES parcela (id), 
	FOREIGN KEY(id_cultivo) REFERENCES cultivo (id)
);
CREATE TABLE notificacion (
	id INTEGER NOT NULL, 
	id_productor INTEGER, 
	mensaje VARCHAR(255) NOT NULL, 
	tipo VARCHAR(50), 
	leido BOOLEAN, 
	fecha DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id_productor) REFERENCES productor (id)
);
INSERT INTO notificacion VALUES(1,NULL,'Nuevo usuario registrado: Javier@gmail.com (antonio) - Plan FREE','registro',0,'2026-04-09 21:09:46.475206');
COMMIT;
