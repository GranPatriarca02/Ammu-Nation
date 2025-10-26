# ARCHIVO PRINCIPAL.

# Accedemos a la clase tablas y usamos el objeto cursor para lanzar las consultas.
from tablas import cursor, mostrarProductos
from funciones import crearProducto, borrarProducto, buscarProducto

# TEMPORAL:
## Mostramos el contenido de las TABLAS de forma temporal, se debe crear un metodo.

# Menu del Ammu Nation: 
def menu():
    while True:
        print("______ AMMU NATION ______")
        print("1. Inventario.")
        print("2. Productos.")
        print("3. Mostrar categorias.")
        print("0. Cerrar menu.")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            print("Se debe agregar el metodo.")
        elif opcion == "2":
            menuProductos()
        elif opcion == "0":
            print("0. Cierras el programa.")
            break
        else:
            print("Has introducido una opcion incorrecta.")

def menuProductos():
    while True:
        print("______ AMMU NATION: MENU DE PRODUCTOS: ______")
        print("1. Agregar un producto.")
        print("2. Mostrar lista de productos.")
        print("3. Buscar un producto.")
        print("4. Editar un producto.")
        print("5. Eliminar un producto.")
        print("0. Volver atras")

        opcion = input("Selecciona una opcion: ").strip()
        if opcion == "1":
            crearProducto()
        elif opcion == "2":
            mostrarProductos()
        elif opcion == "3":
            buscarProducto()
        elif opcion == "4":
            print("NOPE")
        elif opcion == "5":
            borrarProducto()
        elif opcion == "0":
            break
        else:
            print("Has introducido una opcion incorrecta.")





def main():
    menu()
    try:
        # Almacenamos las tablas que vamos a recorrer: 
        tablas = ["CATEGORIAS", "TIPO_ARMA", "CALIBRES", "FABRICANTES", "PRODUCTOS"]
        # Recorremos las tablas
        for recorrerTabla in tablas:
            print(f"\n CONTENIDO: {recorrerTabla}")
            # Consulta que recorre cada una de las tablas del array TABLAS.
            cursor.execute(f"SELECT * FROM {recorrerTabla}")
            filas = cursor.fetchall()
            # Recorremos las filas de las tablas
            if filas:
                for recorrerFila in filas:
                    print(recorrerFila)
            else:
                print("La tabla se encuentra vacia")
    except Exception as e:
        print("ERROR: ", e)
                
main()

