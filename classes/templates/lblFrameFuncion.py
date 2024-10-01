import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .frameFuncion import frameFuncion


class lblFrameFuncion(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.TOP, fill=ttk.BOTH, padx=10, pady=10)

        # Variables de los widgets
        self.frameControles: ttk.Frame = None
        self.add_var: ttk.Button = None
        self.remove_var: ttk.Button = None
        self.frameVariables: ttk.Frame = None
        self.lblZ: ttk.Label = None
        self.funcion: frameFuncion = None

        self.create_widgets()

    def create_widgets(self):
        # Frame de controles de la función
        self.frameControles = ttk.Frame(self)
        self.frameControles.pack(fill=ttk.X, padx=10, pady=(15, 10))
        self.add_var = ttk.Button(self.frameControles, text="+", bootstyle=SUCCESS)
        self.add_var.pack(side=ttk.LEFT, padx=(10, 0))
        self.remove_var = ttk.Button(self.frameControles, text="-", bootstyle=DANGER)
        self.remove_var.pack(side=ttk.LEFT, padx=(10, 0))

        # Frame de variables de la función
        self.frameVariables = ttk.Frame(self)
        self.frameVariables.pack(fill=ttk.X, padx=10, pady=(0, 15))
        self.lblZ = ttk.Label(self.frameVariables, text="Z =", font=('Console', 14))
        self.lblZ.pack(side=ttk.LEFT, padx=10)

        self.funcion = frameFuncion(self.frameVariables)

        # Configura los botones de control añadiendo su metodo asociado
        self.add_var.config(command=self.funcion.add_variable, cursor="hand2")
        self.remove_var.config(command=self.funcion.remove_variable, cursor="hand2")
