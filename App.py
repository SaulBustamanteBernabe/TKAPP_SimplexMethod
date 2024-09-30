import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Establece las propiedades de la aplicación
        self.window_width = None
        self.window_height = None
        # Variables logicas de la App
        self.coeficientes = []

        # Variables de los widgets
        self.lblCoeficientes = []


        # Metodos de inicialización y configuración de la aplicación
        self.title('SIMPLEX APP')
        self.set_window()
        self.create_widgets()


    def create_widgets(self):
        self.frameFunObjetivo = tk.Frame(self, bg='navy')
        self.lblFunObjetivo = tk.Label(self.frameFunObjetivo, text="Función Objetivo", font=('Console', 14), bg="navy", fg='white')
        self.frameCoeficientes = tk.Frame(self.frameFunObjetivo, bg='gold')

        self.lblZ = tk.Label(self.frameCoeficientes, text="Z =", font=('Console', 14), bg="gold", fg='white')
        self.coeficientes.append(tk.StringVar(value="1"))
        self.coeficientes.append(tk.StringVar(value="1"))
        for i, c in enumerate(self.coeficientes):
            self.lblCoeficientes.append(tk.Label(self.frameCoeficientes, text=f"{c.get()}X{i+1}", font=('Console', 14), bg="gold", fg='white'))

        self.frameFunObjetivo.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.lblFunObjetivo.pack(side=tk.TOP)
        self.frameCoeficientes.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.lblZ.pack(side=tk.LEFT, padx=10)
        for lc in self.lblCoeficientes:
            lc.pack(side=tk.LEFT, padx=10)
        
        


    def set_window(self, width=None, height=None, resizable=(False, False)):
        # Obtiene el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Si no se especifica el tamaño, se usa el 70% del tamaño de la pantalla
        if width is None:
            width = int(screen_width * 0.7)
        if height is None:
            height = int(screen_height * 0.7)

        self.window_width = width
        self.window_height = height

        # Calcula la posición centrada
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # Establece la geometría de la ventana
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.resizable(*resizable)


if __name__ == '__main__':
    app = App()
    app.mainloop()
