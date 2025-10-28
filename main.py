# ARCHIVO PRINCIPAL.
# ----------------------------------------------------------------------------------
# Importamos el cursor, inicialización y cierre de la BD desde db.py
from db import cursor, cerrarConexiones, inicializar_base_datos
# Importamos todas las funciones CRUD y reportes desde funciones.py
from funciones import crearProducto, borrarProducto, buscarProducto, editarProducto, mostrarProductos, mostrarPorCategoria, reporteInventario 
# Reporte de inventario para la opción 1 del menú principal

# ----------------------------------------------------------------------------------
# Menu del Ammu Nation: 
def menu():
    """Menú principal de la aplicación."""
    while True:
        print("\n______ AMMU NATION: MENÚ PRINCIPAL ______")
        print("1. Inventario (Reporte y Agregaciones).")
        print("2. Productos (CRUD).")
        print("3. Mostrar categorías.")
        print("0. Cerrar programa.")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            # Llamada al reporte de consultas complejas
            reporteInventario() 
        elif opcion == "2":
            menuProductos()
        elif opcion == "3":
            # Esta opción llama a la función de visualización simple por categoría
            mostrarPorCategoria()
        elif opcion == "0":
            print(" Cerrando el programa. ¡Hasta pronto!")
            break
        else:
            print(" Has introducido una opción incorrecta. Inténtalo de nuevo.")

def menuProductos():
    """Submenú para la gestión CRUD de productos."""
    while True:
        print("\n______ AMMU NATION: MENÚ DE PRODUCTOS (CRUD) ______")
        print("1. Agregar un producto.")
        print("2. Mostrar lista de productos.")
        print("3. Buscar un producto por código de serie.")
        print("4. Editar un producto.")
        print("5. Eliminar un producto.")
        print("0. Volver atrás")

        opcion = input("Selecciona una opción: ").strip()
        
        # --- Operaciones CRUD ---
        if opcion == "1":
            crearProducto()
        elif opcion == "2":
            # Submenú para mostrar listados
            while True:
                print("\n______ AMMU NATION: LISTA DE PRODUCTOS: ______")
                print("1. Mostrar por categoría")
                print("2. Mostrar todos los productos")
                print("0. Volver atrás")
                
                seleccion = input("Selecciona una opción: ").strip()
                if seleccion == "1":
                    mostrarPorCategoria()
                elif seleccion == "2":
                    mostrarProductos()
                elif seleccion == "0":
                    break
                else:
                    print(" Has introducido una opción incorrecta.")

        elif opcion == "3":
            buscarProducto()
        elif opcion == "4":
            editarProducto()
        elif opcion == "5":
            borrarProducto()
        elif opcion == "0":
            break
        else:
            print(" Has introducido una opción incorrecta.")

# ----------------------------------------------------------------------------------
def main():
    """Punto de entrada de la aplicación."""
    try:
        # 1. Inicializa la BD (crea tablas y hace la ingesta inicial)
        inicializar_base_datos() 
        
        # 2. Inicia la interfaz de consola
        menu()
        
    except Exception as e:
        print(f"ERROR CRÍTICO EN LA APLICACIÓN: {e}")
    finally:
        # 3. Limpieza de recursos (conexiones locales y de Turso)
        cerrarConexiones()
        
if __name__ == "__main__":
    main()