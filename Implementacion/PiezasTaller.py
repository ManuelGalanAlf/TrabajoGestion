import tkinter as tk
from tkinter import ttk
import sqlite3

def conectar():
    return sqlite3.connect("C:/Users/manuc/OneDrive/Documentos/UMA/Curso3/GestionInformacion/TrabajoGestion/TrabajoGestion/tallerDB.db")


def insertar():
    # Obtener los valores de las cajas de texto
    nombre = tbNombre.get().strip()
    fabricante = tbFabricante.get().strip()

    # Obtener el material seleccionado en el Listbox
    seleccionado = lbMateriales.curselection()
    if not seleccionado:
        print("Por favor, seleccione un tipo de material.")
        return

    nombreMaterial = lbMateriales.get(seleccionado[0])

    # Verificar si los campos no están vacíos
    if not nombre or not fabricante:
        print("Por favor, complete todos los campos.")
        return

    # Conectar a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Obtener el ID_TIPO del material seleccionado
        cursor.execute("SELECT ID_TIPO FROM tTipoPieza WHERE NOMBRE = ?", (nombreMaterial,))
        id_tipo = cursor.fetchone()

        if not id_tipo:
            print(f"No se encontró el ID_TIPO para el material '{nombreMaterial}'.")
            return

        id_tipo = id_tipo[0]  # Extraer el valor del resultado

        # Insertar el registro en tPiezas
        cursor.execute(
            "INSERT INTO tPiezas (NOMBRE, FABRICANTE, ID_TIPO) VALUES (?, ?, ?)",
            (nombre, fabricante, id_tipo)
        )
        conexion.commit()
        print(f"Pieza '{nombre}' insertada correctamente con ID_TIPO '{id_tipo}'.")



    except Exception as e:
        print(f"Error al insertar los datos: {e}")
        conexion.rollback()

    finally:
        conexion.close()

def borrar():
    # Obtener el elemento seleccionado en el Treeview
    selected_item = tabla.selection()
    if not selected_item:
        print("Por favor, seleccione un elemento para borrar.")
        return

    # Obtener los datos del elemento seleccionado
    valores = tabla.item(selected_item, "values")
    id_seleccionado = valores[0]  # El ID está en la primera columna

    # Conectar a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Eliminar el registro de la base de datos
        cursor.execute("DELETE FROM tPiezas WHERE ID = ?", (id_seleccionado,))
        conexion.commit()
        print(f"Registro con ID {id_seleccionado} eliminado correctamente.")

        # Eliminar el elemento del Treeview
        tabla.delete(selected_item)

        tbNombre.delete(0, tk.END)
        tbFabricante.delete(0, tk.END)
    except Exception as e:
        print(f"Error al borrar el registro: {e}")
        conexion.rollback()

    finally:
        conexion.close()


def actualizar():
    # Obtener el elemento seleccionado en el Treeview
    selected_item = tabla.selection()
    if not selected_item:
        print("Por favor, seleccione un registro para actualizar.")
        return

    # Obtener los valores actuales de los Textbox
    nombre = tbNombre.get().strip()
    fabricante = tbFabricante.get().strip()

    # Verificar si los campos no están vacíos
    if not nombre or not fabricante:
        print("Por favor, complete todos los campos antes de actualizar.")
        return

    # Obtener el ID del registro seleccionado
    valores = tabla.item(selected_item, "values")
    id_seleccionado = valores[0]  # El ID está en la primera columna

    # Obtener el material seleccionado en el Listbox
    seleccionado = lbMateriales.curselection()
    if not seleccionado:
        print("Por favor, seleccione un tipo de material.")
        return

    nombre_material = lbMateriales.get(seleccionado[0])

    # Conectar a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Obtener el ID_TIPO correspondiente al material seleccionado
        cursor.execute("SELECT ID_TIPO FROM tTipoPieza WHERE NOMBRE = ?", (nombre_material,))
        id_tipo = cursor.fetchone()

        if not id_tipo:
            print(f"No se encontró el ID_TIPO para el material '{nombre_material}'.")
            return

        id_tipo = id_tipo[0]  # Extraer el valor del resultado

        # Actualizar el registro en la base de datos
        cursor.execute(
            "UPDATE tPiezas SET NOMBRE = ?, FABRICANTE = ?, ID_TIPO = ? WHERE ID = ?",
            (nombre, fabricante, id_tipo, id_seleccionado)
        )
        conexion.commit()
        print(f"Registro con ID {id_seleccionado} actualizado correctamente.")

        # Actualizar los datos en el Treeview
        tabla.item(selected_item, values=(id_seleccionado, nombre, fabricante, id_tipo))



    except Exception as e:
        print(f"Error al actualizar los datos: {e}")
        conexion.rollback()

    finally:
        conexion.close()


def limpiar():
    tbNombre.delete(0, tk.END)
    tbFabricante.delete(0, tk.END)
    lbMateriales.selection_clear(0, tk.END)  # Esto deselecciona todas las filas del Listbox
    for item in tabla.get_children():
        tabla.delete(item)  # Borra cada fila en la tabla

def salir():
    PiezasTaller.destroy()

def cargar_materiales():
    # Conexión a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    # Consultar todos los materiales de la tabla tTipoPieza
    cursor.execute("SELECT NOMBRE FROM tTipoPieza")
    materiales = cursor.fetchall()

    # Limpiar el Listbox antes de insertar nuevos datos
    lbMateriales.delete(0, tk.END)

    # Agregar cada material al Listbox
    for material in materiales:
        lbMateriales.insert(tk.END, material[0])

    conexion.close()

# Llamar a la función para cargar materiales al inicio

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

def mostrar_componentes(event):
    # Obtener el material seleccionado en el Listbox
    seleccionado = lbMateriales.curselection()
    if seleccionado:
        item = lbMateriales.get(seleccionado[0])
        print(f"Elemento seleccionado: {item}")

        # Conectar a la base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        # Consultar los componentes asociados a ese material
        cursor.execute("""
            SELECT p.ID, p.NOMBRE, p.FABRICANTE, p.ID_TIPO
            FROM tPiezas p
            JOIN tTipoPieza t ON p.ID_TIPO = t.ID_TIPO
            WHERE t.NOMBRE = ?
        """, (item,))

        componentes = cursor.fetchall()

        # Limpiar el Treeview antes de agregar nuevos datos
        for row in tabla.get_children():
            tabla.delete(row)

        # Insertar los componentes en el Treeview
        for componente in componentes:
            tabla.insert("", tk.END, values=componente)

        conexion.close()


# Crear ventana principal
PiezasTaller = tk.Tk()
PiezasTaller.title("Piezas Taller")
PiezasTaller.geometry("700x500")
PiezasTaller.resizable(False, False)

# Etiqueta para "Materia"
lbMaterial = tk.Label(PiezasTaller, text="Material")
lbMaterial.place(x=100, y=50)  # Centrado en la parte superior

# Listbox para seleccionar materiales
lbMateriales = tk.Listbox(PiezasTaller, height=5, selectmode=tk.SINGLE, exportselection=False)
lbMateriales.place(x=250, y=40, width=200, height=100)
cargar_materiales()
lbMateriales.bind("<<ListboxSelect>>", mostrar_componentes)


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


