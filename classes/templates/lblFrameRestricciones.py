import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from .frameRestriccion import frameRestriccion


class lblFrameRestricciones(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.TOP, fill=ttk.BOTH, padx=10, pady=(0, 10), expand=True)

        # Variables de los widgets
        self.frameControles: ttk.Frame = None
        self.add_restic: ttk.Button = None
        self.remove_restric: ttk.Button = None
        self.frameRestricciones: ScrolledFrame = None
        self.restricciones: list[frameRestriccion] = []

        self.create_widgets()

    def create_widgets(self):
        # Frame de controles de la función
        self.frameControles = ttk.Frame(self)
        self.frameControles.pack(side=ttk.TOP, fill=ttk.X, padx=10, pady=(15, 10))
        self.add_restic = ttk.Button(self.frameControles, text="+", bootstyle=SUCCESS)
        self.add_restic.pack(side=ttk.LEFT, padx=(10, 0))
        self.remove_restric = ttk.Button(self.frameControles, text="-", bootstyle=DANGER)
        self.remove_restric.pack(side=ttk.LEFT, padx=(10, 0))

        # Frame de restricciones
        self.frameRestricciones = ScrolledFrame(self)
        self.frameRestricciones.pack(side=ttk.TOP, fill=ttk.BOTH, expand=True, padx=10, pady=(0, 15))
        for i in range(2):
            self.restricciones.append(frameRestriccion(self.frameRestricciones))

        # Configura los botones de control añadiendo su metodo asociado
        self.add_restic.config(command=self.add_restriccion, cursor="hand2")
        self.remove_restric.config(command=self.remove_restriccion, cursor="hand2")
        
    def add_restriccion(self):
        numeroVariables = len(self.restricciones[-1].funcion.entryCoeficientes)
        self.restricciones.append(frameRestriccion(self.frameRestricciones, numVariables=numeroVariables))

    def remove_restriccion(self):
        if len(self.restricciones) > 1:
            self.restricciones[-1].destroy()
            self.restricciones.pop()

    def add_variable(self, event):
        for restriccion in self.restricciones:
            restriccion.funcion.add_variable(value="0")
    
    def remove_variable(self, event):
        for restriccion in self.restricciones:
            restriccion.funcion.remove_variable()
    
    def get_restricciones(self):
        matrizRestricciones = []
        for restriccion in self.restricciones:
            matrizRestricciones.append(restriccion.get_restriccion())
        return matrizRestricciones
