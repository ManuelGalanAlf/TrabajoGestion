import tkinter as tk
from tkinter import ttk

def insertar():
    print("Insertar presionado")

def borrar():
    print("Borrar presionado")

def actualizar():
    print("Actualizar presionado")

def limpiar():
    tbNombre.delete(0, tk.END)
    tbFabricante.delete(0, tk.END)

def salir():
    PiezasTaller.destroy()

# Función para rellenar los campos de texto al seleccionar una fila
def seleccionar_fila(event):
    selected_item = tabla.selection()  # Obtener la selección
    if selected_item:
        # Obtener los valores de la fila seleccionada
        valores = tabla.item(selected_item, "values")
        tbNombre.delete(0, tk.END)  # Limpiar el campo de texto "Nombre"
        tbNombre.insert(0, valores[1])  # Insertar el valor del nombre
        tbFabricante.delete(0, tk.END)  # Limpiar el campo de texto "Fabricante"
        tbFabricante.insert(0, valores[2])  # Insertar el valor del fabricante

# Crear ventana principal
PiezasTaller = tk.Tk()
PiezasTaller.title("Piezas Taller")
PiezasTaller.geometry("700x500")
PiezasTaller.resizable(False, False)

# Etiqueta para "Materia"
lbMaterial = tk.Label(PiezasTaller, text="Materia")
lbMaterial.place(x=100, y=50)  # Centrado en la parte superior

# Listbox para seleccionar materiales
lbMateriales = tk.Listbox(PiezasTaller, height=5, selectmode=tk.SINGLE, exportselection=False)
materiales = ["Chapa", "Motor", "Iluminación", "Sensores", "Cristales"]
for material in materiales:
    lbMateriales.insert(tk.END, material)
lbMateriales.place(x=250, y=40, width=200, height=100)

# Tabla (Treeview)
columns = ("ID", "NOMBRE", "FABRICANTE", "ID_TIPO")
tabla = ttk.Treeview(PiezasTaller, columns=columns, show="headings", height=10)
tabla.heading("ID", text="ID")
tabla.heading("NOMBRE", text="NOMBRE")
tabla.heading("FABRICANTE", text="FABRICANTE")
tabla.heading("ID_TIPO", text="ID_TIPO")

tabla.column("ID", width=50, anchor=tk.CENTER)
tabla.column("NOMBRE", width=250)
tabla.column("FABRICANTE", width=100)
tabla.column("ID_TIPO", width=80, anchor=tk.CENTER)

# Insertar datos iniciales en la tabla
datos = [
    (7, "Bombillas señalización delantera", "RENAULT", "C"),
    (8, "Bombillas luz trasera", "RENAULT", "C"),
    (9, "Bombillas señalización trasera", "RENAULT", "C"),
    (10, "Estuches de bombillas", "RENAULT", "C")
]
for fila in datos:
    tabla.insert("", tk.END, values=fila)

tabla.place(x=50, y=160, width=600, height=150)

# Asociar evento de selección de fila
tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

# Label y Textbox "Nombre"
lbNombre = tk.Label(PiezasTaller, text="Nombre")
lbNombre.place(x=50, y=330)
tbNombre = tk.Entry(PiezasTaller, width=40)
tbNombre.place(x=150, y=330)

# Label y Textbox "Fabricante"
lbFabricante = tk.Label(PiezasTaller, text="Fabricante")
lbFabricante.place(x=50, y=370)
tbFabricante = tk.Entry(PiezasTaller, width=40)
tbFabricante.place(x=150, y=370)

# Botones
btnInsertar = tk.Button(PiezasTaller, text="Insertar", command=insertar)
btnInsertar.place(x=150, y=420, width=80, height=30)

btnBorrar = tk.Button(PiezasTaller, text="Borrar", command=borrar)
btnBorrar.place(x=250, y=420, width=80, height=30)

btnActualizar = tk.Button(PiezasTaller, text="Actualizar", command=actualizar)
btnActualizar.place(x=350, y=420, width=80, height=30)

btnLimpiar = tk.Button(PiezasTaller, text="Limpiar", command=limpiar)
btnLimpiar.place(x=450, y=420, width=80, height=30)

btnSalir = tk.Button(PiezasTaller, text="Salir", command=salir)
btnSalir.place(x=550, y=420, width=80, height=30)

# Iniciar loop principal
PiezasTaller.mainloop()
