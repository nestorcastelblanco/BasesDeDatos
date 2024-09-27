import customtkinter as ctk
import os
import oracledb
import logica.table_ingreso as ingreso
import logica.table_empleados as empleados
import logica.table_pagos as pagos
import logica.table_prestamos as prestamos
import logica.table_solicitud as solicitudes
import logica.table_sucursales as sucursales
import logica.table_usuarios as usuarios
import logica.table_nivel as niveles
import logica.table_cargo as cargos
import logica.table_estado as estados
import logica.table_periodo as periodos

usuario_sistema = []
from tkinter import Image
from datetime import datetime


carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")


def conexion_oracle():
    try:
        connection = oracledb.connect(
            user="SYSTEM", 
            password="0000", 
            dsn="localhost:1521/xe"
        )
        return connection
    except oracledb.DatabaseError as e:
        print(f"Error al conectar a la base de datos: {e}")

def verificar_credenciales(usuario: str, contrasena: str):
    # Obtener el usuario desde la base de datos
    usuario_ingresado = usuarios.obtener_usuario_user(usuario, contrasena)
    
    # Verificar si el usuario existe
    if usuario_ingresado is None:
        return None
    else:
        return usuario_ingresado
        
def obtener_tipo_usuario(usuario: str):
    # Obtener el usuario desde la base de datos
    usuario_ingresado = usuarios.obtener_tipo_user(usuario)
    
    # Verificar si el usuario existe
    if usuario_ingresado is None:
        return None
    else:
        return usuario_ingresado['tipo']

def id_sucursales():
    
    ids = sucursales.get_ids_sucursales()
    if ids is None:
        return ["No hay sucursales aun"]
    else:
        return ids

def enviar_niveles():
    niveles_sistema = niveles.obtener_niveles()
    
    if niveles_sistema is None:
        print("No hay niveles registrados en la BD")
    else:
        return niveles_sistema
     
def enviar_cargos():
    cargos_sistema = cargos.retornar_nombres_cargos()
    
    if cargos_sistema is None:
        print("No hay cargos registrados en el sistema")
    else:
        return cargos_sistema

def funciones_usuario():
    usuarios.create_usuario("nestor_castelblanco", "0000", "Principal")
    # usuarios.create_usuario("NCF", "0000", "Principal")
    # usuarios.obtener_usuario_user(1)
    # usuarios.update_usuario(1, "nestor_castelblanco", "0000", "Empleado")
    # usuarios.delete_usuario(3)
    
def funciones_sucursal():
    sucursales.create_sucursal("Central", "Armenia")
    sucursales.obtener_sucursal(1)
    sucursales.update_sucursal(6, "Central", "Quibdo")
    sucursales.mostrarSucursales()
    sucursales.delete_sucursal(6)
    
def funciones_ingresos():
    ingreso.create_ingreso(1, datetime.now(), datetime.now())
    ingreso.create_ingreso(2, datetime.now(), datetime.now()) 
    ingreso.read_ingreso()
    ingreso.delete_ingreso(1)
    
def funciones_empleados():
    empleados.crear_empleado(1104697502, "Nicolas Rincon", "Operario", 2500000, 1)
    empleados.crear_empleado(1104697503, "Nicolas Rincon 1", "Operario", 2500000, 1)
    empleados.actualizar_empleado(1104697502, "Nicolas Loaiza", "Administrativo", 3500000, 2)
    empleados.eliminar_empleado(1104697503)
    empleados.leer_empleados()

def funciones_solicitud():
    # solicitudes.registrar_solicitud(datetime.now(),1104697502, 12000000, 72)
    # solicitudes.eliminar_solicitud(5)
    # solicitudes.mostrar_solicitudes()
    solicitudes.actualizar_solicitud(8, "aprobada")
    
def funciones_pago():
    pagos.registrar_pago(8, 1, datetime.now(), 750000)

#funciones_usuario()
#funciones_pago()
#funciones_solicitud()
#funciones_empleados()
#funciones_ingresos()    
#funciones_sucursal()
#funciones_auditoria()
##funciones_usuario()asd

import os
from PIL import Image  # Asegúrate de que Image sea importado desde PIL
import customtkinter as ctk

carpeta_principal = os.path.dirname(__file__)
carpeta_imagenes = os.path.join(carpeta_principal, "imagenes")

def enviar_imagen(nombre_imagen: str):
    # print(carpeta_principal)
    # print(carpeta_imagenes)
    
    # # Construir la ruta de la imagen usando f-string
    # image_path = os.path.join(carpeta_imagenes, f"{nombre_imagen}.png")
    
    # logo = ctk.CTkImage(
    #     light_image=Image.open(image_path),
    #     dark_image=Image.open(image_path),
    #     size=(200, 200)
    # )
    # return logo  # Retorna la imagen
    print(os.path.join(carpeta_imagenes, nombre_imagen+".png"))
    return os.path.join(carpeta_imagenes, nombre_imagen+".png")

def crear_empleado(identificacion, nombre, cargo, salario, sucursal, nivel, usuario, contrasena):
    empleados.crear_empleado(identificacion,nombre,cargo, salario, sucursal, nivel, usuario, contrasena)
    

def crear_usuario(identificacion, nombre, usuario, contrasena, nivel):
    usuarios.create_usuario(identificacion,nombre, usuario, contrasena, nivel)

def almacenar_usuario_sistema(id_usuario):
    usuario_sistema.append(id_usuario)
    
def hora_ingreso_usuario():
    usuario_sistema.append(datetime.now())
    
def hora_salida_usuario():
    usuario_sistema.append(datetime.now())
    ingresar_ingreso_sistema()
    
def ingresar_ingreso_sistema():
    id_usuario_sistema = usuario_sistema[0]
    hora_ingreso = usuario_sistema[1]
    hora_salida = usuario_sistema[2]
    ingreso.create_ingreso(id_usuario_sistema, hora_ingreso, hora_salida)

def retornar_tipo_usuario():
    tipo = usuarios.obtener_tipo_user_ID(usuario_sistema[0])
    return tipo