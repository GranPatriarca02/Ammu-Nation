import os
import envyte
import libsql

# Obtener URL y TOKEN.
DB_URL = envyte.get("DB_URL")
API_TOKEN = envyte.get("API_TOKEN")

if not DB_URL or not API_TOKEN:
    raise Exception("ERROR, revisa: DB_URL o API_TOKEN")

# Conexion de la base de datos de la nube
conn = libsql.connect("ammu-nation", sync_url=DB_URL, auth_token=API_TOKEN)

# Sincronizamos los datos
conn.sync()
cursor = conn.cursor()

# Metodo que guarda todos los cambios hechos en la bd.
def actualizarCommit():
    try:
        conn.commit()
        #print("[BD]: Se han actualizado las operaciones.")
    except Exception as e:
        print("ERROR:", e)