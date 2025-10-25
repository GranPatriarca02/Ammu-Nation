# ARCHIVO PRINCIPAL.

# Accedemos a la clase tablas y usamos el objeto cursor para lanzar las consultas.
from tablas import cursor

# TEMPORAL:
## Mostramos el contenido de las TABLAS de forma temporal, se debe crear un metodo.
def main():
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

