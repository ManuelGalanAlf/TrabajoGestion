import tkinter as tk

# Crear ventana principal
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

# Botón OK (moverlo más a la derecha)
bOK = tk.Button(login, text="OK", font=('Roboto', 15), width=10)
bOK.grid(row=3, column=0, padx=30, pady=20)  # Incrementado el padx

# Botón Cancel (moverlo más a la derecha)
bCancel = tk.Button(login, text="Cancel", font=('Roboto', 15), width=10)
bCancel.grid(row=3, column=1, padx=30, pady=20)  # Incrementado el padx

# Iniciar el bucle principal
login.mainloop()
