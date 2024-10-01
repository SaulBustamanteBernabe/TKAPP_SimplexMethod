import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class lblFrameControles(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.TOP, fill=ttk.BOTH, padx=10, pady=(0, 10))

        # Variables de los widgets
        self.optionMethod = None
        self.optionObjetivo = None
        self.btnCalcular = None

        # Variables logicas
        self.options = ["Metodo Simplex", "M grande", "Dos fases"]
        self.objetivos = ["Maximizar", "Minimizar"]

        self.create_widgets()

    def create_widgets(self):
        self.optionMethod = ttk.Combobox(self, bootstyle=READONLY, state='readonly', values=self.options, width=20)
        self.optionMethod.current(0)
        self.optionMethod.pack(side=ttk.LEFT, padx=10, pady=(10, 15))
        self.optionObjetivo = ttk.Combobox(self, bootstyle=READONLY, state='readonly', values=self.objetivos, width=20)
        self.optionObjetivo.current(0)
        self.optionObjetivo.pack(side=ttk.LEFT, padx=10, pady=(10, 15))
        self.btnCalcular = ttk.Button(self, text="Calcular", bootstyle=PRIMARY)
        self.btnCalcular.pack(side=ttk.RIGHT, padx=10, pady=(10, 15))
