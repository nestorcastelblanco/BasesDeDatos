import customtkinter as ctk
import os
import logica.proyecto as proyecto
import interfaces.GUI as ventana_principal
from PIL import Image
from tkinter import ttk
import tkinter as tk
import interfaces.ventanas.parametrico.gestionar_solicitud_parametrico_crear as reg
import interfaces.ventanas.parametrico.gestionar_solicitud_parametrico_editar as edt

# Clase para gestionar la solicitud de empleado
class gestionar_solicitud_parametrico: 
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Solicitud Parametrico")
        
        # Tamaño de la ventana
        self.root.geometry("750x550")
        
        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x = (screen_width // 2) - (750 // 2)  # Centrar en el eje X
        y = (screen_height // 2) - (550 // 2)  # Centrar en el eje Y
        
        # Ajustar la geometría de la ventana
        self.root.geometry(f"750x550+{x}+{y}")
        
        # No permitir redimensionar la ventana
        self.root.resizable(False, False)

        # Título de la ventana
        title_label = ctk.CTkLabel(master=self.root, text="Solicitud Parametrico", font=("Roboto", 28, "bold"))
        title_label.pack(pady=(20, 10))

        # Configurar la conexión a Oracle
        try:
            connection = proyecto.conexion_oracle()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM SOLICITUD")

            columnas = [desc[0] for desc in cursor.description]
            filas = cursor.fetchall()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error de conexión o consulta: {e}")
            return

        # Crear un marco (frame) para contener la tabla
        tabla_frame = ctk.CTkFrame(self.root)
        tabla_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Crear la tabla (Treeview) en el marco
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

        # Establecer el estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')  # Cambia a un tema compatible
        style.configure("Treeview",
                        background="#2e2e2e",  # Fondo oscuro
                        foreground="#ffffff",  # Texto blanco
                        rowheight=25,
                        fieldbackground="#2e2e2e")  # Fondo de las filas

        ancho_columnas = 88
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=ancho_columnas, stretch=True)

        # Insertar los datos en la tabla
        for fila in filas:
            self.tree.insert('', tk.END, values=fila)

        # Empaquetar la tabla con expansión
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Marco para los botones
        botones_frame = ctk.CTkFrame(self.root)
        botones_frame.pack(pady=(10, 20))

        # Botones de acción
        ctk.CTkButton(botones_frame, text="Aprobar", command=self.aprobar_solicitud, font=("Arial", 14, "bold"), width=150).grid(row=0, column=0, padx=10)
        ctk.CTkButton(botones_frame, text="Reprobar", command=self.reaprobar_solicitud, font=("Arial", 14, "bold"), width=150).grid(row=0, column=1, padx=10)
        ctk.CTkButton(botones_frame, text="Editar Solicitud", command=self.enviar_solicitud, font=("Arial", 14, "bold"), width=150).grid(row=0, column=2, padx=10)
        ctk.CTkButton(botones_frame, text="Eliminar Solicitud", command=self.eliminar_solicitud, font=("Arial", 14, "bold"), width=150).grid(row=0, column=3, padx=10)
        ctk.CTkButton(botones_frame, text="Crear Solicitud", command=self.ventana_creacion, font=("Arial", 14, "bold"), width=150).grid(row=0, column=4, padx=10)
        ctk.CTkButton(self.root, text="Ir a Opciones", command=self.ir_a_opciones, font=("Arial", 14, "bold"), width=150).pack(pady=10)

        # Expandir columnas en el frame de botones para un diseño más equilibrado
        for i in range(5):
            botones_frame.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    def aprobar_solicitud(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            if fila[5] == 'PENDIENTE':
                print("Se va aprobar la solicitud")
                self.correo = proyecto.obtenerCorreoSolicitud(fila[0])
                proyecto.editar_estado_solicitud(fila[0], 'APROBADA')
                proyecto.enviar_correo(self.correo, "SOLICITUD APROBADA", "La solicitud que realizo ha sido aprobada, puede comprobar su prestamo en la seccion de PRESTAMOS")
                proyecto.crear_prestamo(fila[1], fila[2], fila[3], fila[4])
                self.root.destroy()
                gestionar_solicitud_parametrico()
            else:
                print("No se puede aprobar la solicitud")
        else:
            print("No se ha seleccionado ninguna fila")

    def reaprobar_solicitud(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            if fila[5] == 'PENDIENTE':
                self.correo = proyecto.obtenerCorreoSolicitud(fila[0])
                print("Se va reprobar la solicitud")
                proyecto.editar_estado_solicitud(fila[0], 'REPROBADA')
                proyecto.enviar_correo(self.correo, "SOLICITUD REPROBADA", "La solicitud que realizo ha sido rechazada")
                self.root.destroy()
                gestionar_solicitud_parametrico()
            else:
                print("No se puede reprobar la solicitud")
        else:
            print("No se ha seleccionado ninguna fila")

    def enviar_solicitud(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            edt.recibir_solicitud(fila)
            self.root.destroy()
            ingresar_ventana_edicion_solicitud = edt.EditarSolicitudParametrico()
            ingresar_ventana_edicion_solicitud.root.mainloop()
        else:
            print("No se ha seleccionado ninguna fila")   

    def obtener_seleccion(self):
        selected_item = self.tree.selection()
        if selected_item:
            fila = self.tree.item(selected_item)['values']
            return fila
        else:
            print("No se ha seleccionado ninguna fila")
            return None

    def eliminar_solicitud(self):
        fila = self.obtener_seleccion()
        if fila and fila[5] == 'PENDIENTE':
            proyecto.eliminar_solicitud(fila)
            self.root.destroy()
            gestionar_solicitud_parametrico()  # Reinicia la ventana
        else:
            print("No se puede eliminar la solicitud debido a que ya fue ajustada o no se ha seleccionado ninguna fila.")

    def ventana_creacion(self):
        self.root.destroy()
        ingresar_ventana_creacion_solicitud = reg.CrearSolicitudParametrico()
        ingresar_ventana_creacion_solicitud.root.mainloop()    

    def ir_a_opciones(self):
        """Cerrar la ventana actual y abrir la ventana de opciones."""
        self.root.destroy()  # Cierra la ventana de gestión de empleados
        tipo_usuario = proyecto.retornar_tipo_usuario()
        ventana_principal.Opciones(tipo_usuario) 
