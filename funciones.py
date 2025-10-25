# Importamos los elementos cursor y actualizarCommit del archivo db.py
from db import cursor, actualizarCommit




# Creamos un bucle para validar los numeros que introduzca el usuario.
def validarInt(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        else:
            print("ERROR: Debes introducir un numero.")

def crearProducto():
    try:
        codigo_serie = input("Codigo de serie: ").strip()
        nombre = input("Nombre del producto:").strip()
        id_calibre = validarInt("Selecciona el calibre: ")
        id_categoria = validarInt("Selecciona la categoria: ")
        id_tipo_arma = validarInt("Selecciona el tipo de arma: ")
        id_categoria =  validarInt("Selecciona el tipo de categoria: ")
        id_fabricante =  validarInt("Selecciona el fabricante: ")
        stock =  validarInt("Cantidad de stock:  ")
        precio =  validarInt("Introduce el precio del producto: ")
        descripcion = input("Introduce la descripcion del producto: ").strip()

        # Creamos la consulta para insertar los datos:
        cursor.execute('''
            INSERT INTO PRODUCTOS (
                CODIGO_SERIE, NOMBRE, ID_CALIBRE, ID_TIPO_ARMA, ID_CATEGORIA, ID_FABRICANTE, STOCK, PRECIO, DESCRIPCION)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo_serie, nombre, id_calibre, id_tipo_arma, id_categoria, id_fabricante, stock, precio, descripcion))
        actualizarCommit()
        print(f"Se ha agregado el producto: {nombre}, con el codigo de serie: {codigo_serie}")
    
    except Exception as e:
        print("ERROR: No se ha podido crear el producto: ", e)

