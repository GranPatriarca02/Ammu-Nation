import os
import envyte
import libsql
import sqlite3 
import random

# --- CONEXIÓN Y CONFIGURACIÓN ---
DB_URL = envyte.get("DB_URL")
API_TOKEN = envyte.get("API_TOKEN")

if not DB_URL or not API_TOKEN:
    raise Exception("ERROR, revisa: DB_URL o API_TOKEN")

DATABASE_FILE = "ammu-nation.db"

# Conexión Turso (Remota)
conn_turso = libsql.connect(DATABASE_FILE, sync_url=DB_URL, auth_token=API_TOKEN)
try:
    conn_turso.sync()
except Exception as e:
    print(f"ADVERTENCIA: No se pudo sincronizar con Turso. Usando solo BD local. Error: {e}")

cursor_turso = conn_turso.cursor()

# Conexión Local (sqlite3)
conn_local = sqlite3.connect(DATABASE_FILE)
cursor_local = conn_local.cursor()

# Exportamos el cursor y la conexión de Turso para el uso principal
cursor = cursor_turso 
conn = conn_turso 


def actualizarCommit():
    """Guarda los cambios en la BD local y los sincroniza con Turso."""
    try:
        conn_turso.commit()
        conn_turso.sync() 
    except Exception as e:
        print("ERROR en commit/sync de Turso:", e)


def cerrarConexiones():
    """Cierra todos los cursores y conexiones abiertos."""
    print("\nCerrando conexiones y cursores...")
    cursor_turso.close()
    conn_turso.close()
    cursor_local.close()
    conn_local.close()
    print("Conexiones cerradas.")


# --- LÓGICA DE INGESTA INICIAL Y CREACIÓN DE TABLAS (Se mantiene igual) ---

def crearTablas(cursor):
    """Define y crea todas las tablas si no existen."""
    try:
        # ... (Definición de tablas) ...
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CATEGORIAS(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT UNIQUE NOT NULL)
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TIPO_ARMA(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT UNIQUE NOT NULL)
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CALIBRES(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT UNIQUE NOT NULL)
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS FABRICANTES(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT UNIQUE NOT NULL)
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PRODUCTOS(
                    CODIGO_SERIE TEXT UNIQUE PRIMARY KEY,
                    NOMBRE TEXT NOT NULL,
                    ID_CALIBRE INTEGER,
                    ID_TIPO_ARMA INTEGER,
                    ID_CATEGORIA INTEGER NOT NULL,
                    ID_FABRICANTE INTEGER NOT NULL,
                    STOCK INTEGER NOT NULL,
                    PRECIO INTEGER NOT NULL,
                    DESCRIPCION TEXT NOT NULL,
                    FOREIGN KEY (ID_CATEGORIA) REFERENCES CATEGORIAS(ID),
                    FOREIGN KEY (ID_TIPO_ARMA) REFERENCES TIPO_ARMA(ID),
                    FOREIGN KEY (ID_CALIBRE) REFERENCES CALIBRES(ID),
                    FOREIGN KEY (ID_FABRICANTE) REFERENCES FABRICANTES(ID))
            ''') 
        
        print("Tablas creadas correctamente.")
    
    except Exception as e:
        print("[ERROR] No se han podido crear las tablas", e)


def obtener_id(nombre_tabla, nombre_valor):
    """Obtiene el ID de una tabla auxiliar dado el nombre."""
    cursor.execute(f"SELECT ID FROM {nombre_tabla} WHERE NOMBRE = ?", (nombre_valor,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def codigoDeSerie(prefijo, longitud=7):
    """Genera un código de serie simple con un prefijo dado."""
    num_aleatorio = "".join(random.choices("1234567890", k=longitud))
    return f"{prefijo}-{num_aleatorio}"


def ingesta_datos_auxiliares():
    """Inserta datos en todas las tablas auxiliares, SIN CONSUMIBLES."""
    
    datos_auxiliares = {
        # 1. CATEGORIAS (Sin Consumibles)
        "CATEGORIAS": ["Armas", "Municion", "Accesorios", "Equipamiento"],
        
        # 2. TIPOS DE ARMA
        "TIPO_ARMA": ["Handguns", "Shotguns", "Submachine Guns", "Assault Rifles", "Sniper Rifles", "Heavy Weapons", "Melee"],
        
        # 3. CALIBRES
        "CALIBRES": [".22 LR", "9×19 mm", ".45 ACP", ".308 Win", "5.56×45 mm", "12 gauge", ".50 BMG", "7.62×39 mm", ".357 Mag", "40 mm Grenade"],
        
        # 4. FABRICANTES
        "FABRICANTES": ["Vandergraaf Arms", "Rustline Works", "Northwind Defense Co.", "Redcrest Ordnance", "Sentinel Gear", "Phoenix Dynamics", "Desert Falcon"]
    }
    
    for tabla, valores in datos_auxiliares.items():
        for v in valores:
            cursor.execute(f"INSERT OR IGNORE INTO {tabla} (NOMBRE) VALUES (?)", (v,))
    actualizarCommit()


def generar_productos_iniciales():
    """Genera una lista amplia de productos de ejemplo (+100 productos)."""
    
    # Mapeo de IDs (Necesario antes de la lista)
    id_cat_arma = obtener_id("CATEGORIAS", "Armas")
    id_cat_municion = obtener_id("CATEGORIAS", "Municion")
    id_cat_accesorio = obtener_id("CATEGORIAS", "Accesorios")
    id_cat_equipamiento = obtener_id("CATEGORIAS", "Equipamiento")

    id_tipo_handgun = obtener_id("TIPO_ARMA", "Handguns")
    id_tipo_assault = obtener_id("TIPO_ARMA", "Assault Rifles")
    id_tipo_sniper = obtener_id("TIPO_ARMA", "Sniper Rifles")
    id_tipo_shotgun = obtener_id("TIPO_ARMA", "Shotguns")
    id_tipo_smg = obtener_id("TIPO_ARMA", "Submachine Guns")
    id_tipo_heavy = obtener_id("TIPO_ARMA", "Heavy Weapons")
    id_tipo_melee = obtener_id("TIPO_ARMA", "Melee")
    
    id_cal_9mm = obtener_id("CALIBRES", "9×19 mm")
    id_cal_556 = obtener_id("CALIBRES", "5.56×45 mm")
    id_cal_308 = obtener_id("CALIBRES", ".308 Win")
    id_cal_12g = obtener_id("CALIBRES", "12 gauge")
    id_cal_50 = obtener_id("CALIBRES", ".50 BMG")
    id_cal_762 = obtener_id("CALIBRES", "7.62×39 mm")
    id_cal_45 = obtener_id("CALIBRES", ".45 ACP")
    id_cal_40mm = obtener_id("CALIBRES", "40 mm Grenade")

    id_fab_vandergraaf = obtener_id("FABRICANTES", "Vandergraaf Arms")
    id_fab_rustline = obtener_id("FABRICANTES", "Rustline Works")
    id_fab_northwind = obtener_id("FABRICANTES", "Northwind Defense Co.")
    id_fab_redcrest = obtener_id("FABRICANTES", "Redcrest Ordnance")
    id_fab_sentinel = obtener_id("FABRICANTES", "Sentinel Gear")
    id_fab_phoenix = obtener_id("FABRICANTES", "Phoenix Dynamics")
    id_fab_falcon = obtener_id("FABRICANTES", "Desert Falcon")


    productos = []
    
    # --- 1. ARMAS (+30 Productos, +10 por Tipo de Arma) ---
    
    # 1.1 Handguns (Pistolas) - +10 productos
    for i in range(1, 12): # 11 productos
        fab = random.choice([id_fab_sentinel, id_fab_vandergraaf, id_fab_falcon])
        cal = random.choice([id_cal_9mm, id_cal_45])
        stock = random.randint(30, 80)
        precio = random.randint(400, 850)
        productos.append((codigoDeSerie("ARM"), f"Pistola T-{i:02d} {random.choice(['Compacta', 'Elite', 'Tactical'])}", cal, id_tipo_handgun, id_cat_arma, fab, stock, precio, "Pistola estándar de servicio."))

    # 1.2 Assault Rifles (Rifles de Asalto) - +10 productos
    for i in range(1, 11): # 10 productos
        fab = random.choice([id_fab_northwind, id_fab_phoenix, id_fab_rustline])
        cal = random.choice([id_cal_556, id_cal_762])
        stock = random.randint(15, 40)
        precio = random.randint(1200, 2500)
        productos.append((codigoDeSerie("ARM"), f"Rifle AR-{i:02d} {random.choice(['Carbine', 'Assault', 'Bullpup'])}", cal, id_tipo_assault, id_cat_arma, fab, stock, precio, "Rifle modular de combate."))

    # 1.3 Sniper Rifles (Francotirador) - +10 productos
    for i in range(1, 11): # 10 productos
        fab = random.choice([id_fab_vandergraaf, id_fab_falcon, id_fab_redcrest])
        cal = random.choice([id_cal_308, id_cal_50])
        stock = random.randint(5, 15)
        precio = random.randint(2800, 5500)
        productos.append((codigoDeSerie("ARM"), f"Rifle SR-{i:02d} {random.choice(['Longshot', 'Ghost', 'Marksman'])}", cal, id_tipo_sniper, id_cat_arma, fab, stock, precio, "Rifle de precisión para largo alcance."))
        
    # 1.4 Heavy Weapons, Shotguns, SMGs, Melee (Resto de Armas)
    productos.extend([
        # Heavy
        (codigoDeSerie("ARM"), "Lanzagranadas RL-40", id_cal_40mm, id_tipo_heavy, id_cat_arma, id_fab_redcrest, 5, 7500, "Sistema de apoyo de fuego pesado."),
        (codigoDeSerie("ARM"), "Ametralladora LMG Phoenix", id_cal_762, id_tipo_heavy, id_cat_arma, id_fab_phoenix, 8, 8900, "Ametralladora ligera de escuadrón."),
        # Shotguns
        (codigoDeSerie("ARM"), "Escopeta R-12 Táctica", id_cal_12g, id_tipo_shotgun, id_cat_arma, id_fab_rustline, 20, 980, "Escopeta semiautomática."),
        (codigoDeSerie("ARM"), "Escopeta Defender P-1", id_cal_12g, id_tipo_shotgun, id_cat_arma, id_fab_sentinel, 35, 750, "Escopeta de corredera confiable."),
        # Melee
        (codigoDeSerie("ARM"), "Machete Táctico VDG", None, id_tipo_melee, id_cat_arma, id_fab_vandergraaf, 150, 95, "Herramienta de supervivencia."),
        (codigoDeSerie("ARM"), "Cuchillo de Combate NW", None, id_tipo_melee, id_cat_arma, id_fab_northwind, 90, 85, "Cuchillo táctico de hoja fija."),
        # SMG
        (codigoDeSerie("ARM"), "Subfusil F-9 SMG", id_cal_9mm, id_tipo_smg, id_cat_arma, id_fab_falcon, 30, 1100, "Subfusil ultracompacto."),
    ])

    # --- 2. MUNICIÓN (+30 Productos, +10 por Calibre Común) ---
    
    # 2.1 Calibre 9x19 mm - +10 productos
    for i in range(1, 11): # 10 productos
        fab = random.choice([id_fab_northwind, id_fab_sentinel])
        stock = random.randint(500, 2000)
        precio = random.randint(30, 60)
        productos.append((codigoDeSerie("MUN"), f"Caja 9mm FMJ Lote {i:02d}", id_cal_9mm, None, id_cat_municion, fab, stock, precio, "Munición FMJ estándar, 1000uds."))

    # 2.2 Calibre 5.56x45 mm - +10 productos
    for i in range(1, 11): # 10 productos
        fab = random.choice([id_fab_vandergraaf, id_fab_phoenix])
        stock = random.randint(400, 1500)
        precio = random.randint(70, 120)
        productos.append((codigoDeSerie("MUN"), f"Caja 5.56mm AP Lote {i:02d}", id_cal_556, None, id_cat_municion, fab, stock, precio, "Munición perforadora, 500uds."))
        
    # 2.3 Calibre 12 gauge - +10 productos
    for i in range(1, 11): # 10 productos
        fab = random.choice([id_fab_rustline, id_fab_redcrest])
        stock = random.randint(300, 1000)
        precio = random.randint(1, 5) # Precio unitario muy bajo
        productos.append((codigoDeSerie("MUN"), f"Postas Cal. 12 Lote {i:02d}", id_cal_12g, None, id_cat_municion, fab, stock, precio, "Cartuchos de postas para escopeta."))
        
    # --- 3. ACCESORIOS Y EQUIPAMIENTO (+30 Productos, +10 por Fabricante) ---
    
    # Lista de Accesorios (con variedad de calibres para supresores/frenos)
    accesorios_base = [
        ("Mira Holográfica D-1", None, 250), ("Bípode de Despliegue Rápido", None, 75), 
        ("Empuñadura Angulada", None, 45), ("Supresor Táctico P-9", id_cal_9mm, 300),
        ("Supresor Pesado .308", id_cal_308, 450), ("Freno de Boca AR", id_cal_556, 150),
        ("Linterna LED 2000Lm", None, 60), ("Kit de Rieles Picatinny", None, 35),
        ("Cargador Extendido 9mm (50rds)", id_cal_9mm, 85), ("Correa Táctica 3 Puntos", None, 25)
    ]
    
    # 3.1 Accesorios (Sentinel Gear) - +10 productos
    for i in range(10): 
        nombre, cal, precio = accesorios_base[i]
        stock = random.randint(20, 70)
        productos.append((codigoDeSerie("ACC"), nombre + " SG", cal, None, id_cat_accesorio, id_fab_sentinel, stock, precio, "Accesorio de combate Sentinel Gear."))

    # 3.2 Accesorios (Vandergraaf Arms) - +10 productos
    for i in range(10): 
        nombre, cal, precio = accesorios_base[i]
        stock = random.randint(20, 70)
        productos.append((codigoDeSerie("ACC"), nombre + " VDG", cal, None, id_cat_accesorio, id_fab_vandergraaf, stock, precio, "Accesorio de alta calidad VDG."))

    # 3.3 Equipamiento (Phoenix Dynamics) - +10 productos
    equipamiento_base = [
        ("Chaleco Balístico N4", None, 1200), ("Casco Táctico Rápido", None, 450), 
        ("Guantes de Asalto", None, 40), ("Botas Militares Alta Montaña", None, 180),
        ("Gafas de Protección Balística", None, 65), ("Rodilleras Reforzadas", None, 30),
        ("Mochila de Gran Capacidad 80L", None, 150), ("Uniforme Táctico", None, 90),
        ("Radio Comunicaciones Digital", None, 700), ("Kit Médico Individual", None, 50)
    ]
    for i in range(10): # 10 productos
        nombre, cal, precio = equipamiento_base[i]
        stock = random.randint(10, 50)
        productos.append((codigoDeSerie("EQP"), nombre + " PD", cal, None, id_cat_equipamiento, id_fab_phoenix, stock, precio, "Equipamiento de asalto Phoenix Dynamics."))


    return productos


def ingesta_productos_inicial():
    """Inserta la lista de productos generada."""
    productos_ejemplo = generar_productos_iniciales()
    
    contador_insertados = 0
    for p in productos_ejemplo:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO PRODUCTOS (
                    CODIGO_SERIE, NOMBRE, ID_CALIBRE, ID_TIPO_ARMA, ID_CATEGORIA, ID_FABRICANTE, STOCK, PRECIO, DESCRIPCION)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', p)
            contador_insertados += 1
        except Exception as e:
            print(f"Error al insertar producto {p[1]} (Skipped): {e}")

    actualizarCommit()
    print(f"Ingesta inicial de {contador_insertados} productos completada.")


def verificar_datos_existentes():
    """Verifica si la tabla PRODUCTOS tiene algún registro."""
    # Usamos el cursor principal (Turso)
    cursor.execute("SELECT COUNT(*) FROM PRODUCTOS")
    return cursor.fetchone()[0] > 0

def inicializar_base_datos():
    """Función principal que crea tablas y realiza la ingesta, solo si es necesario."""
    print("--- INICIALIZANDO BASE DE DATOS ---")
    
    # Crear las tablas (CREATE IF NOT EXISTS)
    crearTablas(cursor) 
    
    #Verificar si ya hay productos (usando la conexión Turso/local)
    if not verificar_datos_existentes():
        print("Detectado: Base de datos vacía. Realizando ingesta inicial de datos.")
        ingesta_datos_auxiliares()
        ingesta_productos_inicial()
    else:
        print("La base de datos ya contiene productos. Ingesta omitida.")
        
    print("-----------------------------------")