import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from PIL import Image
from tkinter import ttk
import tkinter as tk
import interfaces.ventanas.empleado.gestionar_solicitud_empleado_registrar as reg
import interfaces.ventanas.empleado.gestionar_solicitud_empleado_editar as edt

# Clase para gestionar la solicitud de empleado

class gestionar_solicitud_empleado:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Solicitud Empleado")
        self.root.geometry("750x550")
        self.root.resizable(True, True)

        ctk.CTkLabel(master=self.root, text="Vista de solicitudes de Empleado", font=("Roboto", 36)).pack(pady=15)

        # Obtener el ID del usuario
        id_usuario = proyecto.enviar_usuario_sesion()
        print("ID DEL USUARIO: " , id_usuario[0])
        # Configurar la conexión a Oracle y obtener las solicitudes
        self.solicitudes = self.obtener_solicitudes(id_usuario[0])

        # Crear la tabla (Treeview) en la ventana
        self.tree = self.crear_tabla(self.solicitudes)

        # Empaquetar la tabla
        self.tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear un marco (frame) para organizar los botones en fila
        botones_frame = ctk.CTkFrame(self.root)
        botones_frame.pack(pady=10)

        # Añadir los botones alineados en fila utilizando grid
        ctk.CTkButton(botones_frame, text="Editar Solicitud", command=self.enviar_empleado).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botones_frame, text="Eliminar Solicitud", command=self.eliminar_empleado).grid(row=0, column=1, padx=10)
        ctk.CTkButton(botones_frame, text="Crear Solicitud", command=self.ventana_creacion).grid(row=0, column=2, padx=10)
        ctk.CTkButton(self.root, text="Ir a Opciones", command=self.ir_a_opciones).pack(pady=10)

        self.root.mainloop()

    def obtener_solicitudes(self, id_usuario):
        try:
            with proyecto.conexion_oracle() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM SOLICITUD WHERE ID_EMPLEADO = :1", (id_usuario,))
                    columnas = [desc[0] for desc in cursor.description]
                    filas = cursor.fetchall()
                    
                    if not filas:
                        print("No se encontraron solicitudes para el empleado.")
                    
                    return (columnas, filas)
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return ([], [])
        
    def crear_tabla(self, solicitudes):
        columnas, filas = solicitudes
        tree = ttk.Treeview(self.root, columns=columnas, show="headings", height=10)

        # Establecer el estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')  # Cambia a un tema compatible
        style.configure("Treeview",
                        background="#2e2e2e",  # Fondo oscuro
                        foreground="#ffffff",  # Texto blanco
                        rowheight=25,
                        fieldbackground="#2e2e2e")  # Fondo de las filas

        # Crear las cabeceras de la tabla y ajustar el ancho de las columnas
        ancho_columnas = 100
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=ancho_columnas, stretch=False)

        # Insertar los datos en la tabla
        for fila in filas:
            tree.insert('', tk.END, values=fila)

        return tree
    
    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
        else:
            print("No se ha seleccionado ninguna fila")

    def enviar_empleado(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            edt.recibir_solicitud(fila)
            self.root.destroy() 
            ingresar_ventana_edicion_solicitud = edt.EditarSolicitudEmpleados()
            ingresar_ventana_edicion_solicitud.root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")   

    def eliminar_empleado(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            print(f"Fila seleccionada: {fila}")
            self.root.destroy()
            proyecto.eliminar_solicitud(fila)
            gestionar_solicitud_empleado()
        else:
            print("No se ha seleccionado ninguna fila")   
            
    def ventana_creacion(self):
        self.root.destroy() 
        ingresar_ventana_creacion_solicitud = reg.CrearSolicitudEmpleados()
        ingresar_ventana_creacion_solicitud.root.mainloop()    

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()  # Cierra la ventana de gestión de empleados
        tipo_usuario = proyecto.retornar_tipo_usuario() + ""
        ventana_principal.Opciones(tipo_usuario)  # Llama a la ventana de opciones
        
    # Método de ejemplo para volver al menú principal
    def volver_principal(self):
        self.root.destroy()  # Cierra la ventana actual
        gestionar_solicitud_empleado()