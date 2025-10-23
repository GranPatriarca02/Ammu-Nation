# Importamos las herramientas de conexión (cursor y commit) desde el archivo db.py
from db import cursor, actualizarCommit

# =================================================================
# I. FUNCIONES CRUD PARA PRODUCTOS (Gestión de Inventario)
# =================================================================

def crear_producto(codigo, nombre, id_calibre, id_tipo, id_cat, id_fab, stock, precio, desc=""):
    """
    Crea un nuevo producto en el inventario.
    Requisito: Crear (C)
    """
    try:
        query = """
            INSERT INTO PRODUCTOS (CODIGO_SERIE, NOMBRE, ID_CALIBRE, ID_TIPO_ARMA, ID_CATEGORIA, 
                                   ID_FABRICANTE, STOCK, PRECIO, DESCRIPCION)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (codigo, nombre, id_calibre, id_tipo, id_cat, id_fab, stock, precio, desc))
        actualizarCommit()
        return f"Producto '{nombre}' ({codigo}) creado correctamente."
    except Exception as e:
        # Manejo de excepción por integridad (ej. código duplicado o FK inexistente)
        return f"[ERROR C] No se pudo crear el producto. Detalle: {e}"

def leer_producto(codigo_serie):
    """
    Consulta un producto específico por su código.
    Requisito: Leer (R) y Guardar resultados en tupla.
    """
    try:
        cursor.execute("SELECT * FROM PRODUCTOS WHERE CODIGO_SERIE = ?", (codigo_serie,))
        
        # Guarda el resultado en una tupla (o None si no existe)
        producto = cursor.fetchone() 
        
        if producto:
            return ("✅ Producto Encontrado:", producto)
        else:
            return ("⚠️ Producto no encontrado.", None)
    except Exception as e:
        return (f"[ERROR R] Error al consultar el producto: {e}", None)

def actualizar_stock(codigo_serie, cantidad_cambio, es_entrada=True):
    """
    Modifica el stock de un producto (entrada o salida).
    Requisito: Actualizar (U).
    """
    try:
        # Primero, obtenemos el stock actual para calcular el nuevo stock
        producto_data = leer_producto(codigo_serie)
        if not producto_data[1]:
            return f"⚠️ No se pudo actualizar: {producto_data[0]}"

        stock_actual = producto_data[1][6] # Asumiendo que STOCK está en el índice 6
        
        if es_entrada:
            nuevo_stock = stock_actual + cantidad_cambio
        else:
            if stock_actual < cantidad_cambio:
                return "❌ Error: Stock insuficiente para realizar esta salida."
            nuevo_stock = stock_actual - cantidad_cambio

        cursor.execute("UPDATE PRODUCTOS SET STOCK = ? WHERE CODIGO_SERIE = ?", 
                       (nuevo_stock, codigo_serie))
        
        if cursor.rowcount > 0:
            actualizarCommit()
            return f"✅ Stock de {codigo_serie} actualizado a {nuevo_stock}."
        else:
            return f"⚠️ No se encontró el producto {codigo_serie} para actualizar."

    except Exception as e:
        return f"[ERROR U] No se pudo actualizar el stock: {e}"

def eliminar_producto(codigo_serie):
    """
    Elimina un producto del inventario.
    Requisito: Eliminar (D).
    """
    try:
        cursor.execute("DELETE FROM PRODUCTOS WHERE CODIGO_SERIE = ?", (codigo_serie,))
        
        if cursor.rowcount > 0:
            actualizarCommit()
            return f"✅ Producto {codigo_serie} eliminado correctamente."
        else:
            return f"⚠️ Producto {codigo_serie} no encontrado para eliminar."

    except Exception as e:
        return f"[ERROR D] No se pudo eliminar el producto: {e}"

# =================================================================
# II. FUNCIONES DE CONSULTAS COMPLEJAS (Requisito: 5 Tipos Distintos)
# =================================================================

def listar_inventario_completo():
    """Consulta 1: Listado y Unión - Devuelve el inventario con nombres de catálogos (JOINs)."""
    try:
        # Alias para simplificar: P=PRODUCTOS, C=CATEGORIAS, T=TIPO_ARMA, F=FABRICANTES
        query = """
            SELECT 
                P.CODIGO_SERIE, P.NOMBRE, P.PRECIO, P.STOCK, 
                C.NOMBRE AS CATEGORIA, T.NOMBRE AS TIPO, F.NOMBRE AS FABRICANTE
            FROM PRODUCTOS P
            JOIN CATEGORIAS C ON P.ID_CATEGORIA = C.ID
            JOIN TIPO_ARMA T ON P.ID_TIPO_ARMA = T.ID
            JOIN FABRICANTES F ON P.ID_FABRICANTE = F.ID
            ORDER BY P.NOMBRE ASC
        """
        cursor.execute(query)
        # Devolvemos el resultado como una lista de diccionarios (más fácil de manejar en Python)
        columnas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return ("✅ Inventario Completo:", resultados)
    except Exception as e:
        return (f"[ERROR CONSULTA] Falló el listado del inventario: {e}", [])

def calcular_valor_total_por_categoria():
    """
    Consulta 2: Agregación (Agrupación) - Calcula el valor total de inventario por categoría.
    Valor Total = SUM(STOCK * PRECIO)
    """
    try:
        query = """
            SELECT 
                C.NOMBRE AS CATEGORIA, 
                SUM(P.STOCK * P.PRECIO) AS VALOR_TOTAL_INVENTARIO
            FROM PRODUCTOS P
            JOIN CATEGORIAS C ON P.ID_CATEGORIA = C.ID
            GROUP BY C.NOMBRE
            ORDER BY VALOR_TOTAL_INVENTARIO DESC
        """
        cursor.execute(query)
        # Devolvemos el resultado como una lista de tuplas
        return ("✅ Valor por Categoría:", cursor.fetchall())
    except Exception as e:
        return (f"[ERROR CONSULTA] Falló la agregación de valor: {e}", [])

def buscar_por_rango_precio(precio_min, precio_max):
    """Consulta 3: Búsqueda con Condición - Lista productos dentro de un rango de precios."""
    try:
        query = """
            SELECT CODIGO_SERIE, NOMBRE, PRECIO, STOCK 
            FROM PRODUCTOS 
            WHERE PRECIO BETWEEN ? AND ? 
            ORDER BY PRECIO ASC
        """
        cursor.execute(query, (precio_min, precio_max))
        # Devolvemos el resultado como una lista de tuplas
        return (f"✅ Productos entre {precio_min} y {precio_max}:", cursor.fetchall())
    except Exception as e:
        return (f"[ERROR CONSULTA] Falló la búsqueda por rango de precio: {e}", [])

def listar_top_5_mas_caros():
    """Consulta 4: Ordenación y Límite - Lista los 5 productos más caros."""
    try:
        query = "SELECT NOMBRE, PRECIO, CODIGO_SERIE FROM PRODUCTOS ORDER BY PRECIO DESC LIMIT 5"
        cursor.execute(query)
        # Devolvemos el resultado como una lista de tuplas
        return ("✅ Top 5 Productos Más Caros:", cursor.fetchall())
    except Exception as e:
        return (f"[ERROR CONSULTA] Falló el listado TOP 5: {e}", [])

def contar_productos_por_calibre():
    """Consulta 5: Agregación - Cuenta cuántos tipos de productos hay por calibre."""
    try:
        query = """
            SELECT 
                CL.NOMBRE AS CALIBRE, 
                COUNT(P.CODIGO_SERIE) AS CANTIDAD_PRODUCTOS
            FROM PRODUCTOS P
            JOIN CALIBRES CL ON P.ID_CALIBRE = CL.ID
            GROUP BY CL.NOMBRE
            ORDER BY CANTIDAD_PRODUCTOS DESC
        """
        cursor.execute(query)
        # Devolvemos el resultado como una lista de tuplas
        return ("✅ Conteo por Calibre:", cursor.fetchall())
    except Exception as e:
        return (f"[ERROR CONSULTA] Falló el conteo por calibre: {e}", [])

# =================================================================
# III. LIMPIEZA DE RECURSOS (Requisito de la práctica)
# =================================================================

def cerrar_recursos(conn, cursor):
    """Cierra el cursor y la conexión de la base de datos."""
    try:
        cursor.close()
        conn.close()
        return "✅ Conexión a la base de datos y cursor cerrados."
    except Exception as e:
        return f"[ERROR CIERRE] No se pudo cerrar la conexión/cursor: {e}"