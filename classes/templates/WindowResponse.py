import tkinter as tk
from tkinter import Toplevel

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Ventana Principal")
ventana_principal.geometry("400x300")

# Función para crear una ventana emergente
def crear_ventana_emergente():
    ventana_emergente = Toplevel(ventana_principal)
    ventana_emergente.title("Ventana Emergente")
    ventana_emergente.geometry("200x150")
    ventana_emergente.grab_set()
    etiqueta = tk.Label(ventana_emergente, text="¡Hola desde la ventana emergente!")
    etiqueta.pack()

# Botón para abrir la ventana emergente
boton = tk.Button(ventana_principal, text="Abrir Ventana Emergente", command=crear_ventana_emergente)
boton.pack()

# Iniciar el bucle principal de la aplicación
ventana_principal.mainloop()
