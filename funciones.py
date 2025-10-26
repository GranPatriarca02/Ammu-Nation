# Importamos los elementos cursor y actualizarCommit del archivo db.py
from db import cursor, actualizarCommit
from tablas import recorrerTablas, mostrarProductos
import random

# Validamos si existe la fila a la que queremos acceder.
def validarFila(tabla, id_tabla):
    # Ejecutamos la consulta y devolvemos la tabla {FABRICANTES}, id_tabla remplaza la ID que seleccionamos con un input
    # en la ejecución de WHERE ID = ?
    cursor.execute(f"SELECT ID FROM {tabla} WHERE ID = ?", (id_tabla,))
    return cursor.fetchone() is not None # Retornamos un valor booleano, si no es nula devuelve TRUE.

# Validamos si el campo de la tabla existe
# Este metodo contiene validarInt, que valida si el campo introducido es un numero.
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

# Funcion que crea un producto:
def crearProducto():
    try:
        #NOMBRE # Validamos el nombre del producto: 
        validar_nombre = False
        while not validar_nombre:
            nombre = input("Nombre del producto: ").strip()
            if(len(nombre) == 0):
                print("ERROR: El campo nombre no puede estar vacio.")
                validar_nombre = False
            elif(3 <= len(nombre) <= 30):
                validar_nombre = True
            else:
                print("ERROR: El campo nombre debe tener entre 3 y 30 letras.")
        #CALIBRE # La validacion se hace desde validarCampo.
        recorrerTablas("CALIBRES")
        id_calibre = validarCampo("CALIBRES", "Selecciona el calibre: ")
        #CATEGORIAS # La validacion se hace desde validarCampo.
        recorrerTablas("CATEGORIAS")
        id_categoria = validarCampo("CATEGORIAS", "Selecciona la categoria: ")
        #TIPO_ARMA # La validacion se hace desde validarCampo.
        recorrerTablas("TIPO_ARMA")
        id_tipo_arma = validarCampo("TIPO_ARMA", "Selecciona el tipo de ar2ma: ")
        #FABRICANTES # La validacion se hace desde validarCampo.
        recorrerTablas("FABRICANTES")
        id_fabricante =  validarCampo("FABRICANTES", "Selecciona el fabricante: ")
        #STOCK # Validamos la cantidad de stock del producto: 
        validar_stock = False
        while not validar_stock:
            stock =  validarInt("Cantidad de stock: ")
            if(stock >= 0 and stock <= 10000):
                validar_stock = True
            else:
                print("ERROR: El stock debe estar entre 0 y 10.000")
        #PRECIO # Validamos que el precio del producto este entre 1 y 30.000.
        validar_precio = False
        while not validar_precio:
            precio =  validarInt("Introduce el precio del producto: ")
            if(precio > 0 and precio <= 30000):
                validar_precio = True
            else:
                print("ERROR: El precio del producto debe estar entre $1 y $30.000")
        #DESCRIPCION # Validamos la descripcion del producto: 
        validar_descripcion = False
        while not validar_descripcion:
            descripcion = input("Introduce la descripcion del producto: ").strip()
            if(len(descripcion) == 0):
                print("ERROR: La descripcion no puede estar vacia.")
                validar_descripcion = False
            elif(5 <= len(descripcion) <= 1000):
                validar_descripcion = True
            else:
                print("ERROR: La descripcion debe contener entre 5 y 1000 letras")
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

def buscarProducto():
    try:
        codigo_serie = input("Introduce el codigo de serie del produto que quieres buscar: ").strip()
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
                WHERE P.CODIGO_SERIE = ?
            ''', (codigo_serie,))
        producto = cursor.fetchone()

        if producto:
            print("")
            print(f"Nombre del producto: {producto[1]}")
            print(f"Codigo de serie: {producto[0]}")
            print(f"Calibre: {producto[2]}")
            print(f"Tipo de arma: {producto[3]}")
            print(f"Categoria: {producto[4]}")
            print(f"Fabricante: {producto[5]}")
            print(f"Cantidad de stock: {producto[6]}")
            print(f"Precio: {producto[7]}")
            print(f"Descripcion: {producto[8]}")
            print("")
        else:
            print("No se ha encontrado el producto.")     

    except Exception as e:
        print("ERROR: No se ha podido mostrar el producto", e)

def borrarProducto():
    try:
        mostrarProductos()
        # Almacenamos el codigo de serie en una variable borrando los espacios y haciendo que el String este en mayusculas.
        codigo_serie = input("Introduce el codigo de serie del producto que deseas borrar: ").strip().upper()
        
        cursor.execute("SELECT NOMBRE FROM PRODUCTOS WHERE CODIGO_SERIE = ?", (codigo_serie,))
        producto = cursor.fetchone()

        if(producto is None):
            print(f"El codigo de serie: {codigo_serie} no existe.")
        else:
            confirmar = input(f"Seguro que queres eliminar el producto: {producto[0]}? S(i) N(o): ").strip().upper()
            if(confirmar == "S"):
                cursor.execute("DELETE FROM PRODUCTOS WHERE CODIGO_SERIE = ?", (codigo_serie,))
                # Actualizamos los cambios
                actualizarCommit()
                print(f"Has eliminado el producto: {producto[0]}")
            elif(confirmar == "N"):
                print(f"Has cancelado la operacion, no se ha eliminado el producto: {producto[0]}")
            else:
                print(f"Has introducido otro caracter, no se ha eliminado el producto: {producto[0]}")

    except Exception as e:
        print("ERROR: No se ha podido eliminar el producto.", e)

def codigoDeSerie(id_categoria):
    # El codigo de serie variara segun el tipo de categoria:
        # ARM para ARMAS
        # MUN para MUNICIONES
        # ACC para ACCESROIOS
    # Obtenemos el nombre de la categoria, se puede hacer por IDS, pero si cambiamos el nombre de la categoria 
    # recuperaremos el valor eroneamente.
    # Una vez obtenemos la categoría nos generará 7 digitos aleatorios, (Se puede crear una función que también detecte si
    # es posible que el numero sea unico, aunque en la base de datos ya esta restringido con UNIQUE)

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