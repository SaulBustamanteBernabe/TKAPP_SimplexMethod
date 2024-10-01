import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from classes.templates.lblFrameFuncion import lblFrameFuncion
from classes.templates.lblFrameRestricciones import lblFrameRestricciones
from classes.templates.lblFrameControles import lblFrameControles


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="litera")
        # Establece las propiedades de la aplicación
        self.window_width = None
        self.window_height = None

        # Variables de los widgets
        self.funObjetivo = None
        self.funRestricciones = None
        self.panelControles = None

        # Metodos de inicialización y configuración de la aplicación
        self.title('SIMPLEX APP')
        self.set_window(resizable=(True, True))
        self.create_widgets()


    def create_widgets(self):
        # Estructura de la aplicación
        self.funObjetivo = lblFrameFuncion(self, text="Función Objetivo")
        self.funRestricciones = lblFrameRestricciones(self, text="Restricciones")
        self.panelControles = lblFrameControles(self, text="Controles")

        # Funciones adicionales de interrelacion
        self.funObjetivo.add_var.bind("<Button-1>", self.funRestricciones.add_variable, add="+")
        self.funObjetivo.remove_var.bind("<Button-1>", self.funRestricciones.remove_variable, add="+")


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
