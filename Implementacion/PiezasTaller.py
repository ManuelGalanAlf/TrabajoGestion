import tkinter as tk
from tkinter import ttk
import sqlite3
import sys
import DB.db_connection as DB

# Obtener el rol desde los argumentos del sistema (pasado desde login.py)
rol_name = sys.argv[1]  # El rol se pasa como un argumento al ejecutar este script



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
    conexion = DB.conectar()
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

        # Limpiar los campos de entrada (Entry)
        tbNombre.delete(0, tk.END)
        tbFabricante.delete(0, tk.END)

        # Recargar los productos para actualizar la tabla
        cargar_productos(None)  # Ningún evento, solo actualiza la tabla con los nuevos productos.

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
    conexion = DB.conectar()
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
    conexion = DB.conectar()
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

        # Limpiar los campos de texto
        tbNombre.delete(0, tk.END)
        tbFabricante.delete(0, tk.END)

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
    conexion = DB.conectar()
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


def cargar_productos(event):
    # Verificar el rol antes de cargar los productos
    if rol_name == "Invitado":
        print("Rol de invitado: no se pueden cargar los productos.")
        return  # No cargar los productos si el rol es "Invitado"

    # Limpiar los campos de texto
    tbNombre.delete(0, tk.END)
    tbFabricante.delete(0, tk.END)

    # Si no se ha seleccionado un material, cargar todos los productos
    material_seleccionado = lbMateriales.get(lbMateriales.curselection()) if lbMateriales.curselection() else None

    # Conexión a la base de datos
    conexion = DB.conectar()
    cursor = conexion.cursor()

    if material_seleccionado:
        # Consultar los productos de la tabla tPieza basados en el material seleccionado
        cursor.execute("""
            SELECT P.ID, P.NOMBRE, P.FABRICANTE, P.ID_TIPO
            FROM tPiezas P
            JOIN tTipoPieza T ON P.ID_TIPO = T.ID_TIPO
            WHERE T.NOMBRE = ?
        """, (material_seleccionado,))
    else:
        # Si no hay material seleccionado, cargar todos los productos
        cursor.execute("""
            SELECT P.ID, P.NOMBRE, P.FABRICANTE, P.ID_TIPO
            FROM tPiezas P
        """)

    productos = cursor.fetchall()

    # Limpiar la tabla antes de insertar nuevos datos
    for item in tabla.get_children():
        tabla.delete(item)

    # Insertar los productos en la tabla
    for producto in productos:
        tabla.insert("", tk.END, values=producto)

    conexion.close()



def mostrar_producto_seleccionado(event):
    # Obtener el elemento seleccionado en el Treeview
    selected_item = tabla.selection()
    if selected_item:
        # Obtener los datos del producto seleccionado
        valores = tabla.item(selected_item, "values")
        id_producto = valores[0]  # El ID está en la primera columna
        nombre_producto = valores[1]
        fabricante_producto = valores[2]

        # Actualizar los Textboxes con los datos del producto seleccionado
        tbNombre.delete(0, tk.END)
        tbFabricante.delete(0, tk.END)
        tbNombre.insert(0, nombre_producto)
        tbFabricante.insert(0, fabricante_producto)


# Crear ventana principal
PiezasTaller = tk.Tk()
PiezasTaller.title("Piezas Taller")
PiezasTaller.geometry("700x500")
PiezasTaller.resizable(False, False)

# Mostrar el rol en la interfaz
lbRol = tk.Label(PiezasTaller, text=f"Rol: {rol_name}")
lbRol.place(x=50, y=50)

# Etiqueta para "Materia"
lbMaterial = tk.Label(PiezasTaller, text="Material")
lbMaterial.place(x=100, y=50)

# Listbox para seleccionar materiales
lbMateriales = tk.Listbox(PiezasTaller, height=5, selectmode=tk.SINGLE, exportselection=False)
lbMateriales.place(x=250, y=40, width=200, height=100)
cargar_materiales()

# Vincular la selección en el Listbox con la carga de productos
lbMateriales.bind("<<ListboxSelect>>", cargar_productos)

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

# Asignar evento de selección de fila en la tabla para mostrar la información en los Textboxes
tabla.bind("<<TreeviewSelect>>", mostrar_producto_seleccionado)

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

# Desactivar los Textbox si el rol no es "Administrador"
if rol_name != "Administrador":
    tbNombre.config(state=tk.DISABLED)
    tbFabricante.config(state=tk.DISABLED)

# Botones
btnInsertar = tk.Button(PiezasTaller, text="Insertar", command=insertar)
btnInsertar.place(x=150, y=420, width=80, height=30)
btnInsertar.config(state=tk.NORMAL if rol_name == "Administrador" else tk.DISABLED)

btnBorrar = tk.Button(PiezasTaller, text="Borrar", command=borrar)
btnBorrar.place(x=250, y=420, width=80, height=30)
btnBorrar.config(state=tk.NORMAL if rol_name == "Administrador" else tk.DISABLED)

btnActualizar = tk.Button(PiezasTaller, text="Actualizar", command=actualizar)
btnActualizar.place(x=350, y=420, width=80, height=30)
btnActualizar.config(state=tk.NORMAL if rol_name == "Administrador" else tk.DISABLED)

btnLimpiar = tk.Button(PiezasTaller, text="Limpiar", command=limpiar)
btnLimpiar.place(x=450, y=420, width=80, height=30)
btnLimpiar.config(state=tk.NORMAL if rol_name != "Invitado" else tk.DISABLED)

btnSalir = tk.Button(PiezasTaller, text="Salir", command=salir)
btnSalir.place(x=550, y=420, width=80, height=30)

PiezasTaller.mainloop()
