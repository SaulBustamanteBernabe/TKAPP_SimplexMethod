import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

class topLevelResultado(ttk.Toplevel):
    def __init__(self, parent, resultados, title="", **kwargs):
        super().__init__(parent, **kwargs)
        self.title(title)
        self.resultados = resultados
        self.set_window()
        self.create_widgets()

    def create_widgets(self):
        text = ScrolledText(self)
        text.pack(side=ttk.TOP, fill=ttk.BOTH, expand=True)
        for t in self.resultados["res"]:
            text.insert(END, f"{t}\n")

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
