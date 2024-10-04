import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from classes.templates.lblFrameFuncion import lblFrameFuncion
from classes.templates.lblFrameRestricciones import lblFrameRestricciones
from classes.templates.lblFrameControles import lblFrameControles
from classes.templates.topLevelResultado import topLevelResultado
from classes.simplexmethod.SimplexMethod import SimplexMethod
from classes.simplexmethod.BigMethod import BigMethod


class App(ttk.Window):
    def __init__(self):
        super().__init__(iconphoto="./assets/images/Logo_SimplexMethod_32x32.png")
        # Establece las propiedades de la aplicación
        self.window_width = None
        self.window_height = None
        # Estilo de la app
        self.styleApp = ttk.Style()
        self.styleApp.theme_use("litera")
        self.set_styles()

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
        self.panelControles.btnCalcular.bind("<Button-1>", self.calcular, add="+")
    
    def calcular(self, event):
        # Obtiene los coeficientes de la función objetivo
        coeficientes = self.funObjetivo.funcion.get_coeficientes()
        # Obtiene las restricciones
        restricciones = self.funRestricciones.get_restricciones()
        # Obtiene los valores objetivo y metodo
        objetivo = self.panelControles.optionObjetivo.get()
        metodo = self.panelControles.optionMethod.get()
        # Selecciona el metodo y resuelve
        res = {}
        if metodo == "Metodo Simplex":
            simplex = SimplexMethod(objetivo, coeficientes, restricciones)
            res = simplex.resolver()
            res["option"] = None
        elif metodo == "M grande":
            bigM = BigMethod(objetivo, coeficientes, restricciones)
            res = bigM.resolver()
        elif metodo == "Dos fases":
            print("Dos fases")
        # Mensaje de error y retorna
        if "Error" in res.keys():
            Messagebox.show_error(parent=self, title="Error", message=res["Error"])
            return
        # Mensaje de advertencias
        if "Warning" in res.keys():
            Messagebox.show_warning(parent=self, title="Advertencia", message=res["Warning"])
        # Ventana de resultados
        resultados = topLevelResultado(self, res["res"], title="Resultados", option=res["option"])
        


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

    def set_styles(self):
        # Configurar el estilo del Treeview
        self.styleApp.configure("Treeview",
            background="#E8E8E8",  # Fondo gris claro
            foreground="#333333",  # Texto gris oscuro
            rowheight=30,         # Altura de las filas
            fieldbackground="#F0F0F0",  # Fondo de las celdas
            font=("Helvetica", 12)  # Fuente y tamaño de letra
        )
        # Configurar el estilo de las cabeceras
        self.styleApp.configure("Treeview.Heading",
            font=("Helvetica", 14, "bold"),  # Fuente negrita para las cabeceras
            background="#DCDCDC"  # Fondo gris claro para las cabeceras
        )


if __name__ == '__main__':
    app = App()
    app.mainloop()
