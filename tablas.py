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
                            CODIGO_SERIE TEXT PRIMARY KEY,
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
        
    except Exception as e:
        print("[ERROR] No se han podido crear las tablas", e)