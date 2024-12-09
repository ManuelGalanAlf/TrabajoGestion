import sqlite3
import os
# Conectar a la base de datos
conn = sqlite3.connect("gestionDB.db")
cursor = conn.cursor()

# Cargar el script SQL desde un archivo y ejecutarlo
with open("../tallerDB.sql", "r") as file:
    sql_script = file.read()

cursor.executescript(sql_script)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()
