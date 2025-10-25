# Importamos los elementos cursor y actualizarCommit del archivo db.py
from db import cursor, actualizarCommit

def crearProducto():
    try:
        codigo_serie = input("Codigo de serie: ").strip()
        nombre = input("Nombre del producto:").strip()
        id_calibre = int(input("Selecciona el calibre: "))
        id_tipo_arma = int(input("Selecciona el tipo de arma: "))
        id_categoria = int(input("Selecciona el tipo de categoria: "))
        id_fabricante = int(input("Selecciona el fabricante: "))
        stock = int(input("Cantidad de stock: "))
        precio = int(input("Introduce el precio del producto: "))
        descripcion = input("Introduce la descripcion del producto: ").strip()

        # Creamos la consulta para insertar los datos:
        cursor.execute('''
            INSERT IN TO PRODUCTOS (
                CODIGO_SERIE, NOMBRE, ID_CALIBRE, ID_TIPO_ARMA, ID_CATEGORIA, ID_FABRICANTE, STOCK, PRECIO, DESCRIPCION)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo_serie, nombre, id_calibre, id_tipo_arma, id_categoria, id_fabricante, stock, precio, descripcion))
        actualizarCommit()
        print(f"Se ha agregado el producto: {nombre}, con el codigo de serie: {codigo_serie}")
    
    except Exception as e:
        print("ERROR: No se ha podido crear el producto: ", e)

