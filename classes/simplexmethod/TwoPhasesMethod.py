import pandas as pd
import numpy as np
from .SimplexMethod import SimplexMethod


class TwoPhasesMethod:

    MAXIMIZAR = "Maximizar"
    MINIMIZAR = "Minimizar"

    def __init__(self, objetivo, coeficientes, restricciones):
        # Valores iniciales
        self.objetivo = objetivo
        self.coeficientes = coeficientes
        self.restricciones = restricciones
        # Valores construidos
        self.numpy_restricciones = None
        self.tipo_restricciones = None
        self.numpy_coeficientes = None
        self.dosFases_resoluble = None
        self.variables_artificiales = []
        self.fase_2_resolved = False
        self.tablas_fase_1: list[pd.DataFrame] = []
        self.res_1 = dict()
        self.tablas_fase_2: list[pd.DataFrame] = []
        self.res_2 = dict()
        self.res = dict()

    def resolver(self):
        # Fase 1: Resolver problema auxiliar con objetivo de minimizar
        self.fase_1()
        # Fase 2: Resolver problema principal con objetivo de maximizar
        self.fase_2()
        # Retorna como respuesta el listado de tablas del problema
        self.res_1["res"] = self.tablas_fase_1
        self.res["res_1"] = self.res_1
        self.res_2["res"] = self.tablas_fase_2
        self.res_2["resolved"] = self.fase_2_resolved
        self.res["res_2"] = self.res_2
        return self.res
    
    def fase_1(self):
        # Generar tabla del problema auxiliar
        tAux = self.generar_tabla_auxiliar()
        simplexResolve = SimplexMethod("Minimizar", None, None)
        simplexResolve.tablas.append(tAux.astype(float))
        simplexResolve.desarrollar_tablas()
        self.tablas_fase_1.extend(simplexResolve.tablas)
        self.res_1 = simplexResolve.res
    
    def generar_tabla_auxiliar(self):
        # Generar tabla auxiliar con funcion Auxiliar
        self.validar_restricciones()
        # Contruir Dataframe del problema, construyo el nombre de las columnas
        columnas = [f"x{i+1}" for i in range(len(self.coeficientes))] + ["R"]
        tabla = pd.DataFrame(self.numpy_restricciones, columns=columnas)
        tabla.loc[len(tabla)] = np.zeros(len(self.coeficientes)+1)
        tabla.rename(index={len(tabla)-1: f"Aux"}, inplace=True)
        # Bucle para agregar variables de holgura, exceso y artificiales a la tabla, junto con los valores de la nueva funcion auxiliar, se almacenan las variables artificiales en una lista
        exceso = 0
        for r in range(len(self.restricciones)):
            if self.tipo_restricciones[r] == "<=":
                col = [1 if i == r else 0 for i in range(len(self.restricciones))] + [0]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", col)
                tabla.rename(index={r: f"S{r+1+exceso}"}, inplace=True)
            elif self.tipo_restricciones[r] == "=":
                col = [1 if i == r else 0 for i in range(len(self.restricciones))] + [-1]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", col)
                tabla.rename(index={r: f"S{r+1+exceso}"}, inplace=True)
                self.variables_artificiales.append(f"S{r+1+exceso}")
            elif self.tipo_restricciones[r] == ">=":
                colExceso = [-1 if i == r else 0 for i in range(len(self.restricciones))] + [0]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", colExceso)
                exceso += 1
                col = [1 if i == r else 0 for i in range(len(self.restricciones))] + [-1]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", col)
                tabla.rename(index={r: f"S{r+1+exceso}"}, inplace=True)
                self.variables_artificiales.append(f"S{r+1+exceso}")
        # Tabla auxiliar incial de referencia
        self.tablas_fase_1.append(tabla.copy())
        # Se suman las filas artificiales a la funcion auxiliar
        for v in self.variables_artificiales:
            tabla.loc["Aux"] = tabla.loc["Aux"] + tabla.loc[v]
        return tabla

    def validar_restricciones(self):
        # Se extrae la matriz de restricciones y se deja por separado el tipo de restricción
        # Se guardan el las propiedades de numpy_restricciones y tipo_restricciones para usarlas mas adelante
        self.numpy_restricciones = []
        self.tipo_restricciones = []
        for restriccion in self.restricciones:
            linea = np.array(restriccion[0])
            linea = np.append(linea, restriccion[2])
            self.numpy_restricciones.append(linea)
            self.tipo_restricciones.append(restriccion[1])
        # Se valida la condicion de no negatividad
        for i, restriccion in enumerate(self.numpy_restricciones):
            if restriccion[-1] < 0:
                self.numpy_restricciones[i] = -restriccion
                if self.tipo_restricciones[i] == "<=": self.tipo_restricciones[i] = ">="
                elif self.tipo_restricciones[i] == ">=": self.tipo_restricciones[i] = "<="

    def fase_2(self):
        # Obtener el resultado de la fase 1
        tabla_auxiliar = self.tablas_fase_1[-1].copy()
        # Verificar si es resoluble por dos fases
        if tabla_auxiliar.iloc[-1, -1] != 0:
            self.res_2["Warning"] = "No Resoluble por Dos Fases: El reltado de la fase 1 no es igual a cero"
            return
        # Adaptar la tabla de la fase 1 a la fase 2
        tabla_fase_2 = tabla_auxiliar.drop(columns=self.variables_artificiales, inplace=False)
        tabla_fase_2 = tabla_fase_2.drop(index="Aux", inplace=False)
        tabla_fase_2.loc["Z"] = np.concatenate((np.array(self.coeficientes)*-1, np.zeros(len(tabla_fase_2.columns)-len(self.coeficientes))))
        # Guardar la tabla, como tabla de referencia inicial
        self.tablas_fase_2.append(tabla_fase_2.copy())
        # Validar solucion factible inicial
        for i, fila in tabla_fase_2.iterrows():
            if "x" in i:
                tabla_fase_2.loc["Z"] = tabla_fase_2.loc["Z"] - (tabla_fase_2.loc[i] * tabla_fase_2.loc["Z", i])
        simplexResolve = SimplexMethod(self.objetivo, None, None)
        simplexResolve.tablas.append(tabla_fase_2.astype(float))
        simplexResolve.desarrollar_tablas()
        self.fase_2_resolved = simplexResolve.res["Status"]
        self.tablas_fase_2.extend(simplexResolve.tablas)
        self.fase_2_resolved = True
