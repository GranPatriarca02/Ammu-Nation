# ARCHIVO PRINCIPAL.

# Accedemos a la clase tablas y usamos el objeto cursor para lanzar las consultas.
from tablas import cursor
from funciones import crearProducto

# TEMPORAL:
## Mostramos el contenido de las TABLAS de forma temporal, se debe crear un metodo.

# Menu del Ammu Nation: 
def menu():
    while True:
        print("______ AMMU NATION ______")
        print("1. Inventario.")
        print("2. Agregar producto.")
        print("3. Mostrar categorias.")
        print("0. Cerrar menu.")

        opcion = input("Introduce una opcion: ").strip()

        if opcion == "1":
            print("Se debe agregar el metodo.")
        elif opcion == "2":
            crearProducto()
        elif opcion == "3":
            print("Se debe agregar el metodo.")
        elif opcion == "0":
            print("0. Cierras el programa.")
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

