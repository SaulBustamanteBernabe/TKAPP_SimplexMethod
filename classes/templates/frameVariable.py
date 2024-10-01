import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class frameVariable(ttk.Frame):
    def __init__(self, parent, variable, numero, coef="1", **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.LEFT ,fill=ttk.BOTH, padx=10, pady=(5, 5))

        # Variables de los widgets
        self.entryCoeficiente: ttk.Entry = None
        self.lblVariable: ttk.Label = None

        # Variables logicas de la App
        self.coeficiente = ttk.StringVar(value=coef)
        self.variable = variable
        self.numero = numero

        self.create_widgets()

    def create_widgets(self):
        self.entryCoeficiente = ttk.Entry(self, textvariable=self.coeficiente, width=5)
        self.entryCoeficiente.pack(side=ttk.LEFT)
        self.lblVariable = ttk.Label(self, text=f"{self.variable}{self.numero}", font=('Console', 14))
        self.lblVariable.pack(side=ttk.LEFT)

    def get_coeficiente(self):
        try:
            return float(self.entryCoeficiente.get())
        except ValueError:
            raise ValueError(f"El coeficiente {self.variable}{self.numero} debe ser un número")
