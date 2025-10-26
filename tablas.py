# Importamos solo las funciones que queremos desde db.py
from db import cursor, actualizarCommit

#TABLAS
def crearTablas():
    try:
        # Tabla CATEGORIAS
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS CATEGORIAS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE TEXT UNIQUE NOT NULL)
                    ''')
        
        # Tabla TIPO ARMA
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS TIPO_ARMA(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE TEXT UNIQUE NOT NULL)
                    
                    ''')
        # Tabla TIPO CALIBRES
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS CALIBRES(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE TEXT UNIQUE NOT NULL)
                    ''')
        
        # Tabla TIPO FABRICANTES
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS FABRICANTES(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NOMBRE TEXT UNIQUE NOT NULL)
                    ''')
        
        # Tabla TIPO PRODUCTOS
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS PRODUCTOS(
                            CODIGO_SERIE TEXT UNIQUE PRIMARY KEY,
                            NOMBRE TEXT NOT NULL,
                            ID_CALIBRE INTEGER NOT NULL,
                            ID_TIPO_ARMA INTEGER NOT NULL,
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
        
        # - COMENTARIOS TEMPORALES.
        # VALORES POR DEFECTO: Se podran insertar mas en el CRUD ((funcion temporal?)).
        # PODRIAMOS OBTENER DICHOS VALORES DESDE UN FICHERO .txt, en caso de necesitarlo.
        datos = {
            "CATEGORIAS": ["Armas", "Municion", "Accesorios"],
            "TIPO_ARMA": ["Handguns","Shotguns","Submachine Guns","Assault Rifles","Light Machine Guns", "Sniper Rifles", "Sniper Rifles", "Melee"],
            "CALIBRES": [".25 ACP",".32 ACP","9×19 mm",".357 Magnum",".40 S&W",
                        "12 gauge","20 gauge",
                        "7.62×25 mm","5.7×28 mm","5.56×45 mm",
                        "7.62×39 mm","7.62×51 mm",".300 Winchester Magnum",".50 BMG"],
            "FABRICANTES": ["Vandergraaf Arms","Rustline Works","Northwind Defense Co.","Redcrest Ordnance"]
        }
        
        for tabla, valores in datos.items():
            for v in valores:
                # Ejecutamos la consulta a la base de datos para insertar los valores.
                # IGNORE ignora un valor que pueda estar repetido.
                cursor.execute(f"INSERT OR IGNORE INTO {tabla} (NOMBRE) VALUES (?)", (v,))
                
        actualizarCommit() # Confirmamos y aplicamos los cambios.
        print("Tablas creadas y datos predefinidos insertados correctamente.")
    
    except Exception as e:
        print("[ERROR] No se han podido crear las tablas", e)

def recorrerTablas(nombreTabla):
     try:
        # Preparamos nuestra consulta y la guardamos en la variable filas.
        cursor.execute(f"SELECT * FROM {nombreTabla}")
        filas = cursor.fetchall()
        # Si filas es verdadero mostramos el contenido de la tabla y recorremos la fila una por una para mostrarla.
        if filas:
            print(f"SELECCION DE: {nombreTabla}")
            for fila in filas:
                print(f"{fila[0]}: {fila[1]}")
        else:
            print("La tabla: {nombreTabla} esta vacia.")

     except Exception as e:
         print(f"ERROR: No se ha podido recorrer la tabla: {nombreTabla} o no existe", e)
# Mostramos los productos: 
def mostrarProductos():
    try:    
        cursor.execute('''
            SELECT 
                P.CODIGO_SERIE, 
                P.NOMBRE, 
                C.NOMBRE AS CALIBRE, 
                T.NOMBRE AS TIPO_ARMA, 
                CAT.NOMBRE AS CATEGORIA, 
                F.NOMBRE AS FABRICANTE,
                P.STOCK,
                P.PRECIO,
                P.DESCRIPCION
            FROM PRODUCTOS P
            JOIN CALIBRES C ON P.ID_CALIBRE = C.ID
            JOIN TIPO_ARMA T ON P.ID_TIPO_ARMA = T.ID
            JOIN CATEGORIAS CAT ON P.ID_CATEGORIA = CAT.ID
            JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
        ''')

        contador = 0
        filas = cursor.fetchall()
        if filas:
            for fila in filas:
                contador +=1
                print(f"{contador}): Codigo de serie: {fila[0]}, Nombre: {fila[1]}, Calibre: {fila[2]}, Tipo de arma: {fila[3]}, Categoria: {fila[4]}, Fabricante: {fila[5]}, Stock: {fila[6]}, Precio: {fila[7]}$")
                print(f"Descripcion: {fila[8]} \n")
        else:
            print("No hay productos creados.")
        
    except Exception as e:
        print("ERROR: No se ha podido recorrer la tabla PRODUCTOS", e)
