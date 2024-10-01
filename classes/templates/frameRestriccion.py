import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .frameFuncion import frameFuncion
from .frameVariable import frameVariable


class frameRestriccion(ttk.Frame):
    def __init__(self, parent, numVariables=2, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.TOP, fill=ttk.BOTH, padx=10, pady=10)

        # Variables de los widgets
        self.funcion: frameFuncion = None
        self.relacion: ttk.Combobox = None
        self.coefRestriccion: frameVariable = None

        # Variables logicas
        self.relaciones = ["<=", "=", ">="]

        self.create_widgets(numVariables)

    def create_widgets(self, numVariables):
        # Frame de la función
        self.funcion = frameFuncion(self, numVariables=numVariables, defaultEntry="0")
        # Combobox de la relación
        self.relacion = ttk.Combobox(self, bootstyle=READONLY, state='readonly', values=self.relaciones, width=3)
        self.relacion.current(0)
        self.relacion.pack(side=ttk.LEFT, padx=10)
        # Entrada del coeficiente de restricción
        self.coefRestriccion = frameVariable(self, variable="", numero="", coef="0")

    def get_restriccion(self):
        fun = self.funcion.get_coeficientes()
        relacion = self.relacion.get()
        coef = self.coefRestriccion.get_coeficiente()
        return fun, relacion, coef