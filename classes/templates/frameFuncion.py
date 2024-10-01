import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .frameVariable import frameVariable


class frameFuncion(ttk.Frame):
    def __init__(self, parent, numVariables=2, defaultEntry="1", **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.LEFT, fill=ttk.X)

        # Variables de los widgets
        self.entryCoeficientes: list[frameVariable] = []

        # Variables logicas
        self.defaultEntry = defaultEntry

        self.create_widgets(numVariables)

    def create_widgets(self, num_vars):
        for i in range(num_vars):
            var = frameVariable(self, variable="X", numero=i+1, coef=self.defaultEntry)
            self.entryCoeficientes.append(var)   
    
    def add_variable(self, value="1"):
        var = frameVariable(self, variable="X", numero=self.entryCoeficientes[-1].numero+1, coef=value)
        self.entryCoeficientes.append(var)

    def remove_variable(self):
        if len(self.entryCoeficientes) > 1:
            self.entryCoeficientes[-1].destroy()
            self.entryCoeficientes.pop()
    
    def get_coeficientes(self):
        coeficientes = []
        for var in self.entryCoeficientes:
            coeficientes.append(var.get_coeficiente())
        return coeficientes
