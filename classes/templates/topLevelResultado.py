import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
import sympy as sp

class topLevelResultado(ttk.Toplevel):
    def __init__(self, parent, resultados, title="", option=None, **kwargs):
        super().__init__(parent, **kwargs)
        # Inicializa la ventana
        self.window_width = None
        self.window_height = None
        self.title(title)
        # Variables de los widgets
        self.notebook_tablas: ttk.Notebook = None
        self.tablas: list[ttk.Frame] = []
        # Variables logicas
        self.resultados: list[pd.DataFrame] = resultados
        self.option = option
        self.set_window()
        self.create_widgets()

    def create_widgets(self):
        self.notebook_tablas = ttk.Notebook(self, bootstyle=SUCCESS)
        self.notebook_tablas.pack(side=ttk.TOP, fill=ttk.BOTH, expand=True)
        for i, tabla in enumerate(self.resultados):
            columnas = ['Base'] + tabla.columns.tolist()
            frame_tabla = ttk.Treeview(self.notebook_tablas, columns=columnas, show='headings', bootstyle=SUCCESS, style='Treeview')
            for c in columnas:
                frame_tabla.heading(c, text=c)
                frame_tabla.column(c, anchor=CENTER, width=0)
            for j, r in tabla.iterrows():
                contenido = r
                if self.option == "M":
                    contenido = contenido.to_list()
                    contenido = [c.evalf(5) if isinstance(c, sp.Expr) else c for c in contenido]
                else:
                    contenido = contenido.round(3).to_list()
                frame_tabla.insert('', END, values=([j] + contenido))
            frame_tabla.pack(side=ttk.TOP, fill=ttk.BOTH, expand=True)
            self.notebook_tablas.add(frame_tabla, text=f"Tabla {i+1}")

    def set_window(self, width=None, height=None):
        # Obtiene el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Si no se especifica el tamaño, se usa el 70% del tamaño de la pantalla
        if width is None:
            width = int(screen_width * 0.5)
        if height is None:
            height = int(screen_height * 0.5)

        self.window_width = width
        self.window_height = height

        # Calcula la posición centrada
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # Establece la geometría de la ventana
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
