import random
import sqlite3
# Importamos el cursor de Turso (para operaciones CRUD), la conexión local (para funciones propias)
# y la función para guardar cambios (commit/sync).
from db import cursor, actualizarCommit, conn_local, cursor_local




## 2. FUNCIONES DE VALIDACIÓN Y UTILERÍA

def validarFila(tabla, id_tabla):
    """Verifica si un ID existe en una tabla dada."""
    cursor.execute(f"SELECT ID FROM {tabla} WHERE ID = ?", (id_tabla,))
    return cursor.fetchone() is not None # Retorna True si existe, False si no

def validarCampo(tabla, mensaje):
    """Solicita un ID y lo valida contra la base de datos."""
    while True: 
        id_val = validarInt(mensaje)
        if validarFila(tabla, id_val):
            return id_val
        else:
            print(f"Advertencia: El ID: {id_val} no existe en la tabla: {tabla}")

def validarInt(mensaje):
    """Crea un bucle para validar si la entrada del usuario es un número entero."""
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        else:
            print("ERROR: Debes introducir un número.")

def codigoDeSerie(id_categoria):
    """Genera un código de serie basado en la categoría."""
    cursor.execute("SELECT NOMBRE FROM CATEGORIAS WHERE ID = ?", (id_categoria,))
    consulta = cursor.fetchone()
    if consulta is None:
        return print(f"Advertencia: La categoría no existe")
        
    devolver_categoria = consulta[0].upper()

    if "ARMAS" in devolver_categoria:
        nombreCategoria = "ARM"
    elif "MUNICION" in devolver_categoria:
        nombreCategoria = "MUN"
    elif "ACCESORIOS" in devolver_categoria:
        nombreCategoria = "ACC"
    elif "EQUIPAMIENTO" in devolver_categoria:
        nombreCategoria = "EQP"
    else:
        nombreCategoria = "GEN"
        
    # Generamos el número aleatorio
    numAleatorio = "".join(random.choices("1234567890", k=7))
    return f"{nombreCategoria}-{numAleatorio}"


## 3. FUNCIONES DE VISUALIZACIÓN (READ)

def recorrerTablas(nombreTabla):
    """Muestra todos los registros de una tabla auxiliar (CATEGORIAS, FABRICANTES, etc.)."""
    try:
        cursor.execute(f"SELECT ID, NOMBRE FROM {nombreTabla}")
        filas = cursor.fetchall()
        if filas:
            print(f"\nSELECCIÓN DE: {nombreTabla}")
            for fila in filas:
                print(f"{fila[0]}: {fila[1]}")
        else:
            print(f"Advertencia: La tabla: {nombreTabla} está vacía.")
    except Exception as e:
        print(f"ERROR: No se ha podido recorrer la tabla: {nombreTabla} o no existe", e)

def mostrarProductos():
    """Lista todos los productos con sus detalles (JOIN en todas las tablas)."""
    try: 
        cursor.execute('''
            SELECT 
                P.CODIGO_SERIE, P.NOMBRE, 
                C.NOMBRE AS CALIBRE, T.NOMBRE AS TIPO_ARMA, 
                CAT.NOMBRE AS CATEGORIA, F.NOMBRE AS FABRICANTE,
                P.STOCK, P.PRECIO, P.DESCRIPCION
            FROM PRODUCTOS P
            LEFT JOIN CALIBRES C ON P.ID_CALIBRE = C.ID
            LEFT JOIN TIPO_ARMA T ON P.ID_TIPO_ARMA = T.ID
            LEFT JOIN CATEGORIAS CAT ON P.ID_CATEGORIA = CAT.ID
            LEFT JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
            ORDER BY P.CODIGO_SERIE ASC
        ''')

        filas = cursor.fetchall()
        if filas:
            print("\n--- LISTADO COMPLETO DE PRODUCTOS ---")
            for i, fila in enumerate(filas, 1):
                print(f"\n{i}): CÓDIGO: {fila[0]}, Nombre: {fila[1]}")
                print(f"   Categoría: {fila[4]} | Tipo Arma: {fila[3] if fila[3] else 'N/A'} | Calibre: {fila[2] if fila[2] else 'N/A'}")
                print(f"   Fabricante: {fila[5]} | Stock: {fila[6]} | Precio: ${fila[7]:.2f}")
        else:
            print("Advertencia: No hay productos creados.")
        
    except Exception as e:
        print("ERROR: No se ha podido listar los productos", e)

def mostrarPorCategoria():
    """Muestra los productos filtrados por una categoría seleccionada."""
    try:
        # 1. Mostrar categorías disponibles
        cursor.execute("SELECT ID, NOMBRE FROM CATEGORIAS ORDER BY ID")
        categorias = cursor.fetchall()
        if not categorias:
             print("Advertencia: No hay categorías disponibles.")
             return

        print("\n--- SELECCIONE UNA CATEGORÍA ---")
        for id_cat, nombre_cat in categorias:
             print(f"{id_cat}: {nombre_cat}")

        # 2. Validar selección
        id_valor = validarCampo("CATEGORIAS", "Selecciona la categoría (ID): ")

        # 3. Obtener los productos de esa categoría
        cursor.execute('''
            SELECT 
                P.CODIGO_SERIE, P.NOMBRE, C.NOMBRE AS CALIBRE, T.NOMBRE AS TIPO_ARMA, 
                CAT.NOMBRE AS CATEGORIA, F.NOMBRE AS FABRICANTE,
                P.STOCK, P.PRECIO
            FROM PRODUCTOS P
            LEFT JOIN CALIBRES C ON P.ID_CALIBRE = C.ID
            LEFT JOIN TIPO_ARMA T ON P.ID_TIPO_ARMA = T.ID
            LEFT JOIN CATEGORIAS CAT ON P.ID_CATEGORIA = CAT.ID
            LEFT JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
            WHERE P.ID_CATEGORIA = ?
            ORDER BY P.NOMBRE
        ''', (id_valor,))

        filas = cursor.fetchall()
        if filas:
            print(f"\n--- PRODUCTOS EN CATEGORÍA: {filas[0][4].upper()} ---")
            for i, fila in enumerate(filas, 1):
                print(f"{i}): CÓDIGO: {fila[0]}, Nombre: {fila[1]}, Stock: {fila[6]}, Precio: ${fila[7]:.2f}")
        else:
            print("Advertencia: No hay productos en esta categoría.")

    except Exception as e:
        print("ERROR: No se ha podido mostrar los productos por categoría", e)

## 4. FUNCIONES CRUD RESTANTES (CREATE, UPDATE, DELETE)

def crearProducto():
    """Función que crea un nuevo producto, con validaciones."""
    try:
        # 1. NOMBRE
        while True:
            nombre = input("Nombre del producto: ").strip()
            if 3 <= len(nombre) <= 30:
                break
            else:
                print("ERROR: El nombre debe tener entre 3 y 30 letras.")

        # 2. CATEGORIAS
        recorrerTablas("CATEGORIAS")
        id_categoria = validarCampo("CATEGORIAS", "Selecciona la categoría (ID): ")
        
        cursor.execute("SELECT NOMBRE FROM CATEGORIAS WHERE ID = ?", (id_categoria,))
        obtener_categoria = cursor.fetchone()[0].strip().upper()
        
        # 3. VALIDACIONES CONDICIONALES (TIPO ARMA, CALIBRE)
        id_tipo_arma = None
        id_calibre = None
        
        if "ARMAS" in obtener_categoria:
            recorrerTablas("TIPO_ARMA")
            id_tipo_arma = validarCampo("TIPO_ARMA", "Selecciona el tipo de arma (ID): ")
            
            cursor.execute("SELECT NOMBRE FROM TIPO_ARMA WHERE ID = ?", (id_tipo_arma,))
            tipo_nombre = cursor.fetchone()[0].upper()

            if "MELEE" not in tipo_nombre:
                recorrerTablas("CALIBRES")
                id_calibre = validarCampo("CALIBRES", "Selecciona el calibre (ID): ")
                
        elif "MUNICION" in obtener_categoria:
            recorrerTablas("CALIBRES")
            id_calibre = validarCampo("CALIBRES", "Selecciona el calibre (ID): ")
        
        # 4. FABRICANTES
        recorrerTablas("FABRICANTES")
        id_fabricante = validarCampo("FABRICANTES", "Selecciona el fabricante (ID): ")
        
        # 5. STOCK
        while True:
            stock = validarInt("Cantidad de stock (0-10000): ")
            if 0 <= stock <= 10000:
                break
            else:
                print("ERROR: El stock debe estar entre 0 y 10.000.")
        
        # 6. PRECIO
        while True:
            precio = validarInt("Introduce el precio del producto (0-30000): ")
            if 0 <= precio <= 30000:
                break
            else:
                print("ERROR: El precio debe estar entre $0 y $30.000.")
        
        # 7. DESCRIPCION
        while True:
            descripcion = input("Introduce la descripción del producto (5-1000): ").strip()
            if 5 <= len(descripcion) <= 1000:
                break
            else:
                print("ERROR: La descripción debe contener entre 5 y 1000 letras.")
                
        # 8. CÓDIGO DE SERIE
        codigo_serie = codigoDeSerie(id_categoria)

        # 9. INSERCIÓN
        cursor.execute('''
            INSERT INTO PRODUCTOS (
                CODIGO_SERIE, NOMBRE, ID_CALIBRE, ID_TIPO_ARMA, ID_CATEGORIA, ID_FABRICANTE, STOCK, PRECIO, DESCRIPCION)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (codigo_serie, nombre, id_calibre, id_tipo_arma, id_categoria, id_fabricante, stock, precio, descripcion))
        
        actualizarCommit()
        print(f"Se ha agregado el producto: {nombre}, con el código de serie: {codigo_serie}")
    
    except sqlite3.IntegrityError as ie:
        # Manejo de error específico por clave duplicada o FK fallida
        print(f"ERROR DE INTEGRIDAD: El producto ya existe o hay datos de referencia inválidos. {ie}")
    except Exception as e:
        print("ERROR: No se ha podido crear el producto:", e)

def buscarProducto():
    """Busca y muestra los detalles de un producto por su código de serie."""
    try:
        codigo_serie = input("Introduce el código de serie del producto que quieres buscar: ").strip().upper()
        cursor.execute('''
            SELECT 
                P.CODIGO_SERIE, P.NOMBRE, 
                C.NOMBRE AS CALIBRE, T.NOMBRE AS TIPO_ARMA, 
                CAT.NOMBRE AS CATEGORIA, F.NOMBRE AS FABRICANTE,
                P.STOCK, P.PRECIO, P.DESCRIPCION
            FROM PRODUCTOS P
            LEFT JOIN CALIBRES C ON P.ID_CALIBRE = C.ID
            LEFT JOIN TIPO_ARMA T ON P.ID_TIPO_ARMA = T.ID
            LEFT JOIN CATEGORIAS CAT ON P.ID_CATEGORIA = CAT.ID
            LEFT JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
            WHERE P.CODIGO_SERIE = ?
            ''', (codigo_serie,))
        producto = cursor.fetchone()

        if producto:
            print("\n--- DETALLES DEL PRODUCTO ENCONTRADO ---")
            print(f"Código de serie: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Categoría: {producto[4]}")
            print(f"Fabricante: {producto[5]}")
            print(f"Stock: {producto[6]}")
            print(f"Precio: ${producto[7]:.2f}")
            print(f"Calibre: {producto[2] if producto[2] else 'N/A'}")
            print(f"Tipo de arma: {producto[3] if producto[3] else 'N/A'}")
            print(f"Descripción: {producto[8]}")
            print("---------------------------------------")
        else:
            print(f"Advertencia: No se ha encontrado el producto con código: {codigo_serie}.")    

    except Exception as e:
        print("ERROR: No se ha podido mostrar el producto", e)

def borrarProducto():
    """Elimina un producto por su código de serie."""
    try:
        mostrarProductos()
        codigo_serie = input("Introduce el código de serie del producto que deseas borrar: ").strip().upper()
        
        cursor.execute("SELECT NOMBRE FROM PRODUCTOS WHERE CODIGO_SERIE = ?", (codigo_serie,))
        producto = cursor.fetchone()

        if producto is None:
            print(f"Advertencia: El código de serie: {codigo_serie} no existe.")
        else:
            confirmar = input(f"¿Seguro que quiere eliminar el producto: {producto[0]}? S(í)/N(o): ").strip().upper()
            if confirmar == "S":
                cursor.execute("DELETE FROM PRODUCTOS WHERE CODIGO_SERIE = ?", (codigo_serie,))
                actualizarCommit()
                print(f"Has eliminado el producto: {producto[0]}.")
            elif confirmar == "N":
                print(f"Operación cancelada. No se ha eliminado el producto: {producto[0]}.")
            else:
                print("Respuesta no válida. Operación cancelada.")

    except Exception as e:
        print("ERROR: No se ha podido eliminar el producto.", e)

def editarProducto():
    """Edita los campos seleccionados de un producto existente."""
    try:
        mostrarProductos()
        codigo_serie = input("Introduce el código de serie del producto a editar: ").strip().upper()

        cursor.execute('SELECT NOMBRE, ID_CATEGORIA FROM PRODUCTOS WHERE CODIGO_SERIE = ?', (codigo_serie,))
        producto_info = cursor.fetchone()
        
        if not producto_info:
            print(f"Advertencia: El código de serie: {codigo_serie} no existe.")
            return
        
        nombre_producto, id_categoria_actual = producto_info
        
        # Obtenemos la categoría para saber qué campos puede editar
        cursor.execute("SELECT NOMBRE FROM CATEGORIAS WHERE ID = ?", (id_categoria_actual,))
        categoria_nombre = cursor.fetchone()[0].strip().upper()
        
        while True:
            print(f"\n______ AMMU NATION: EDITANDO: {nombre_producto} ({codigo_serie}) ______")
            print("1. Nombre.")
            print("2. Precio.")
            print("3. Stock.")
            print("4. Descripción.")
            print("5. Fabricante.")
            
            # Solo si la categoría es ARMAS o MUNICIÓN se muestran estas opciones
            if "ARMAS" in categoria_nombre or "MUNICION" in categoria_nombre:
                print("6. Calibre.")
            if "ARMAS" in categoria_nombre:
                print("7. Tipo de arma.")

            print("0. Volver atrás.")
            
            opcion = input("Selecciona la opción a editar: ").strip()
            
            if opcion == "0":
                break

            # 1. EDITAR NOMBRE
            if opcion == "1":
                while True:
                    editar_valor = input(f"Introduce el nuevo nombre (actual: {nombre_producto}): ").strip()
                    if 3 <= len(editar_valor) <= 30:
                        cursor.execute("UPDATE PRODUCTOS SET NOMBRE = ? WHERE CODIGO_SERIE = ?", (editar_valor, codigo_serie))
                        actualizarCommit()
                        print(f"Nombre actualizado a: {editar_valor}")
                        break
                    else:
                        print("ERROR: El nombre debe tener entre 3 y 30 caracteres.")
            
            # 2. EDITAR PRECIO
            elif opcion == "2":
                editar_precio = validarInt("Introduce el nuevo precio: ")
                if 0 <= editar_precio <= 30000:
                    cursor.execute("UPDATE PRODUCTOS SET PRECIO = ? WHERE CODIGO_SERIE = ?", (editar_precio, codigo_serie))
                    actualizarCommit()
                    print(f"Precio actualizado a: ${editar_precio:.2f}")
                else:
                    print("ERROR: El precio debe estar entre $0 y $30.000")
            
            # 3. EDITAR STOCK
            elif opcion == "3":
                editar_stock = validarInt("Introduce el nuevo stock: ")
                if 0 <= editar_stock <= 10000:
                    cursor.execute("UPDATE PRODUCTOS SET STOCK = ? WHERE CODIGO_SERIE = ?", (editar_stock, codigo_serie))
                    actualizarCommit()
                    print(f"Stock actualizado a: {editar_stock}")
                else:
                    print("ERROR: El stock debe estar entre 0 y 10.000")
            
            # 4. EDITAR DESCRIPCION
            elif opcion == "4":
                while True:
                    editar_valor = input("Introduce la nueva descripción (5-1000): ").strip()
                    if 5 <= len(editar_valor) <= 1000:
                        cursor.execute("UPDATE PRODUCTOS SET DESCRIPCION = ? WHERE CODIGO_SERIE = ?", (editar_valor, codigo_serie))
                        actualizarCommit()
                        print("Descripción actualizada.")
                        break
                    else:
                        print("ERROR: La descripción debe contener entre 5 y 1000 letras.")

            # 5. EDITAR FABRICANTE
            elif opcion == "5":
                recorrerTablas("FABRICANTES")
                id_fabricante = validarCampo("FABRICANTES", "Selecciona el nuevo fabricante (ID): ")
                cursor.execute("UPDATE PRODUCTOS SET ID_FABRICANTE = ? WHERE CODIGO_SERIE = ?", (id_fabricante, codigo_serie))
                
                cursor.execute("SELECT NOMBRE FROM FABRICANTES WHERE ID = ?", (id_fabricante,))
                nombre_fabricante = cursor.fetchone()[0]
                actualizarCommit()
                print(f"Fabricante actualizado a: {nombre_fabricante}")
            
            # 6. EDITAR CALIBRE (solo para Armas y Munición)
            elif opcion == "6" and ("ARMAS" in categoria_nombre or "MUNICION" in categoria_nombre):
                recorrerTablas("CALIBRES")
                id_calibre = validarCampo("CALIBRES", "Selecciona el nuevo calibre (ID): ")
                cursor.execute("UPDATE PRODUCTOS SET ID_CALIBRE = ? WHERE CODIGO_SERIE = ?", (id_calibre, codigo_serie))
                
                cursor.execute("SELECT NOMBRE FROM CALIBRES WHERE ID = ?", (id_calibre,))
                nombre_calibre = cursor.fetchone()[0]
                actualizarCommit()
                print(f"Calibre actualizado a: {nombre_calibre}")

            # 7. EDITAR TIPO ARMA (solo para Armas)
            elif opcion == "7" and "ARMAS" in categoria_nombre:
                recorrerTablas("TIPO_ARMA")
                id_tipo_arma = validarCampo("TIPO_ARMA", "Selecciona el nuevo tipo de arma (ID): ")
                cursor.execute("UPDATE PRODUCTOS SET ID_TIPO_ARMA = ? WHERE CODIGO_SERIE = ?", (id_tipo_arma, codigo_serie))
                
                cursor.execute("SELECT NOMBRE FROM TIPO_ARMA WHERE ID = ?", (id_tipo_arma,))
                nombre_tipo = cursor.fetchone()[0]
                actualizarCommit()
                print(f"Tipo de arma actualizado a: {nombre_tipo}")
            
            elif opcion not in ["1", "2", "3", "4", "5"]:
                print("Opción no válida o no aplicable a esta categoría de producto.")

    except Exception as e:
        print("ERROR al editar el producto:", e)


## 5. FUNCIONES DE REPORTE Y CONSULTAS COMPLEJAS

def reporteInventario():
    """Realiza consultas complejas (agregaciones, uniones, condiciones) para el reporte."""
    try:
        print("\n______ AMMU NATION: REPORTE DE INVENTARIO: ______")
        
        # 1. Reporte de Stock Bajo (Condición y Agregación)
        # Productos con stock < 15, listando nombre y fabricante
        print("\n--- 1. Productos con STOCK BAJO ( < 15 unidades) ---")
        consulta_stock_bajo = '''
            SELECT P.NOMBRE, F.NOMBRE, P.STOCK
            FROM PRODUCTOS P
            JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
            WHERE P.STOCK < 15
            ORDER BY P.STOCK ASC
        '''
        cursor.execute(consulta_stock_bajo)
        stock_bajo = cursor.fetchall()
        
        if stock_bajo:
            for nombre_prod, nombre_fab, stock in stock_bajo:
                print(f"- {nombre_prod} (Fabricante: {nombre_fab}) - Stock: {stock}")
        else:
            print("Stock bajo: No hay productos con menos de 15 unidades.")

        # 2. Valor total del Inventario y Conteo (Agregación y Unión)
        print("\n--- 2. Valor Total del Inventario por Categoría ---")
        consulta_valor_total = '''
            SELECT 
                CAT.NOMBRE AS CATEGORIA, 
                SUM(P.STOCK * P.PRECIO) AS VALOR_TOTAL_CATEGORIA,
                COUNT(P.CODIGO_SERIE) AS CANTIDAD_PRODUCTOS
            FROM PRODUCTOS P
            JOIN CATEGORIAS CAT ON P.ID_CATEGORIA = CAT.ID
            GROUP BY CAT.NOMBRE
            ORDER BY VALOR_TOTAL_CATEGORIA DESC
        '''
        cursor.execute(consulta_valor_total)
        
        for categoria, valor, count in cursor.fetchall():
            print(f"- {categoria}: ${valor:.2f} (Total de {count} productos)")
        
        # 3. Fabricantes sin Productos (JOIN y Subconsulta/Condición)
        print("\n--- 3. Fabricantes sin productos en el inventario ---")
        consulta_sin_productos = '''
            SELECT F.NOMBRE
            FROM FABRICANTES F
            LEFT JOIN PRODUCTOS P ON F.ID = P.ID_FABRICANTE
            WHERE P.ID_FABRICANTE IS NULL
        '''
        cursor.execute(consulta_sin_productos)
        sin_productos = [f[0] for f in cursor.fetchall()]
        
        if sin_productos:
            print("Fabricantes:", ", ".join(sin_productos))
        else:
            print("Todos los fabricantes tienen al menos un producto.")
            
        # 4. Calibre más común por Tipo de Arma (Agrupación y Ordenación)
        print("\n--- 4. Calibre más común por Tipo de Arma ---")
        consulta_calibre_comun = '''
            SELECT 
                T.NOMBRE AS TIPO_ARMA, 
                C.NOMBRE AS CALIBRE_COMUN,
                COUNT(P.ID_CALIBRE) AS TOTAL_USO
            FROM PRODUCTOS P
            JOIN TIPO_ARMA T ON P.ID_TIPO_ARMA = T.ID
            JOIN CALIBRES C ON P.ID_CALIBRE = C.ID
            GROUP BY T.NOMBRE, C.NOMBRE
            ORDER BY T.NOMBRE, TOTAL_USO DESC
        '''
        cursor.execute(consulta_calibre_comun)
        
        resultados_calibre = {}
        # Agrupamos los resultados para mostrar solo el más común por tipo de arma
        for tipo, calibre, uso in cursor.fetchall():
            # Solo almacena el calibre más usado para cada tipo de arma
            if tipo not in resultados_calibre or uso > resultados_calibre[tipo][1]:
                 resultados_calibre[tipo] = (calibre, uso)

        for tipo, (calibre, uso) in resultados_calibre.items():
            print(f"- Tipo de arma: {tipo} -> Calibre más usado: {calibre} ({uso} productos)")
        # 5. Valor Promedio de Productos por Fabricante (Ejecución LOCAL)
        print("\n--- 5. Valor Promedio de Productos por Fabricante (Ejecución LOCAL) ---")

        # Importamos el cursor local aquí para asegurar que se usa esta conexión
        # Consulta simplificada: Calcula el precio promedio de TODOS los productos por fabricante,
        # sin aplicar filtros de MAX o AVG.
        consulta_avg_simple_local = '''
        SELECT 
            F.NOMBRE AS FABRICANTE, 
            AVG(P.PRECIO) AS PRECIO_PROMEDIO,
            COUNT(P.CODIGO_SERIE) AS TOTAL_PRODUCTOS
            FROM PRODUCTOS P
            JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
            GROUP BY F.NOMBRE
            ORDER BY PRECIO_PROMEDIO DESC
        '''
        # Usamos el cursor_local para demostrar la funcionalidad de la conexión local.

        cursor_local.execute(consulta_avg_simple_local)
        resultados_promedio = cursor_local.fetchall()

        if resultados_promedio:
            print("Cálculo de Promedio de Precio (Ejecutado con cursor_local):")
            print("----------------------------------------------------------")
            for fabricante, promedio, total in resultados_promedio:
                print(f"- {fabricante} | Productos: {total} | Precio Promedio: ${promedio:.2f}")
                print("----------------------------------------------------------")
        else:
            print("Advertencia: No hay fabricantes que tengan productos con precio superior a $1000 en la BD local.")

    except Exception as e:
        print("ERROR al generar el reporte de inventario:", e)