# Importamos los elementos cursor y actualizarCommit del archivo db.py
from db import cursor, actualizarCommit
import random

# Validamos si existe la fila a la que queremos acceder.
def validarFila(tabla, id_tabla):
    # Ejecutamos la consulta y devolvemos la tabla {FABRICANTES}, id_tabla remplaza la ID que seleccionamos con un input
    # en la ejecución de WHERE ID = ?
    cursor.execute(f"SELECT ID FROM {tabla} WHERE ID = ?", (id_tabla,))
    return cursor.fetchone() is not None # Retornamos un valor booleano, si no es nula devuelve TRUE.

def validarCampo(tabla, mensaje):
    while True: 
        id = validarInt(mensaje)
        if validarFila(tabla, id):
            return id
        else:
            print(f"El ID: {id} no existe en la tabla: {tabla}")


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
        nombre = input("Nombre del producto: ").strip()
        id_calibre = validarCampo("CALIBRES", "Selecciona el calibre: ")
        id_categoria = validarCampo("CATEGORIAS", "Selecciona la categoria: ")
        id_tipo_arma = validarCampo("TIPO_ARMA", "Selecciona el tipo de arma: ")
        id_fabricante =  validarCampo("FABRICANTES", "Selecciona el fabricante: ")
        stock =  validarInt("Cantidad de stock: ")
        precio =  validarInt("Introduce el precio del producto: ")
        descripcion = input("Introduce la descripcion del producto: ").strip()
        codigo_serie = codigoDeSerie(id_categoria)

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


def codigoDeSerie(id_categoria):
    # El codigo de serie variara segun el tipo de categoria:
        # ARM para ARMAS
        # MUN para MUNICIONES
        # ACC para ACCESROIOS
    # Obtenemos el nombre de la categoria, se puede hacer por IDS, pero si cambiamos el nombre de la categoria 
    # recuperaremos el valor eroneamente.

    cursor.execute("SELECT NOMBRE FROM CATEGORIAS WHERE ID = ?", (id_categoria,))
    consulta = cursor.fetchone()
    # Si al recorrer la consula no obtenemos la ID retornamos false y dejamos de ejecutar la funcion.
    if consulta is None:
        return print(f"La categoria no existe")
    # Transformamos la consulta del String en mayusculas.
    devolver_categoria = consulta[0].upper()

    if "ARMAS" in devolver_categoria:
        nombreCategoria = "ARM"
    elif "MUNICION" in devolver_categoria:
        nombreCategoria = "MUN"
    elif "ACCESORIOS" in devolver_categoria:
        nombreCategoria = "ACC"
    else:
        # No deberia de entrar, a no ser que añadamos más tipos de categorías.
        nombreCategoria = "000"
    # Generamos el numero aleatorio:
    numAleatorio = ""
    for numerosAleatorios in range(7):
        numAleatorio = numAleatorio + random.choice("1234567890")
    # Retornamos fuera del bucle el codigo de serie:    
    return f"{nombreCategoria}-{numAleatorio}"


