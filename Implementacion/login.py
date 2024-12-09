import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

# Función para conectar a la base de datos
def conectar():
    return sqlite3.connect("C:/Users/manuc/OneDrive/Documentos/UMA/Curso3/GestionInformacion/TrabajoGestion/TrabajoGestion/tallerDB.db")


# Función para validar el login con base de datos
def validar_login():
    usuario = tbUsuario.get().strip()
    password = tbPassword.get().strip()

    # Validación simple: Comprobar si las credenciales existen en la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Comprobar si el usuario existe y la contraseña es correcta
        cursor.execute("SELECT password, rolName FROM tUsuario WHERE nombre = ?", (usuario,))
        result = cursor.fetchone()

        if result:
            db_password, rol_name = result
            if db_password == password:
                messagebox.showinfo("Login Exitoso", f"Bienvenido {usuario}. El rol de su cuenta es de {rol_name}.")
                login.destroy()  # Cierra la ventana de login
                abrir_pantalla_principal(rol_name)  # Llama a la función para abrir la ventana principal
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")

    finally:
        conexion.close()


# Función para abrir la pantalla principal
def abrir_pantalla_principal(rol_name):
    #if rol_name == "Invitado":
     #   messagebox.showerror("Acceso Denegado", "No tienes permiso para acceder a la sección de Piezas Taller.")
     #   return  # Si el rol es "Invitado", no abrimos la pantalla principal

    # Ejecuta el archivo PiezasTaller.py, pasando el rol como argumento
    try:
        subprocess.run(["python", "PiezasTaller.py", rol_name])  # Pasa el rol como argumento
    except FileNotFoundError:
        messagebox.showerror("Error",
                             "No se encontró el archivo 'PiezasTaller.py'. Asegúrate de que está en el mismo directorio.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al abrir la ventana principal: {e}")


# Crear la ventana de login
login = tk.Tk()
login.title("Login")
login.geometry("450x300")

# Título principal
lbTitle = tk.Label(login, text="Bienvenido", font=('Roboto', 38, 'bold'))
lbTitle.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky='n')

# label y textbox usuario
lbUsuario = tk.Label(login, text="Usuario", font=('Roboto', 15))
lbUsuario.grid(row=1, column=0, padx=10, pady=10, sticky='w')
tbUsuario = tk.Entry(login, font=('Roboto', 15))
tbUsuario.grid(row=1, column=1, padx=10, pady=10)

# Etiqueta y caja de texto para Contraseña
lbPassword = tk.Label(login, text="Password", font=('Roboto', 15))
lbPassword.grid(row=2, column=0, padx=10, pady=10, sticky='w')
tbPassword = tk.Entry(login, font=('Roboto', 15), show="*")
tbPassword.grid(row=2, column=1, padx=10, pady=10)

# Botón OK (para iniciar sesión)
bOK = tk.Button(login, text="OK", font=('Roboto', 15), width=10, command=validar_login)
bOK.grid(row=3, column=0, padx=30, pady=20)

# Botón Cancel
bCancel = tk.Button(login, text="Cancel", font=('Roboto', 15), width=10, command=login.quit)
bCancel.grid(row=3, column=1, padx=30, pady=20)

# Iniciar el bucle principal
login.mainloop()
