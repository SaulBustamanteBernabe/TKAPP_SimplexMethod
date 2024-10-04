import sympy as sp
import pandas as pd
import numpy as np


class BigMethod:

    MAXIMIZAR = "Maximizar"
    MINIMIZAR = "Minimizar"

    def __init__(self, objetivo, coeficientes, restricciones):
        # Valores iniciales
        self.objetivo = objetivo
        self.coeficientes = coeficientes
        self.restricciones = restricciones
        self.M = sp.symbols("M")
        self.valueM = 100000000
        # Valores construidos
        self.numpy_restricciones = None
        self.tipo_restricciones = None
        self.numpy_coeficientes = None
        self.tablas: list[pd.DataFrame] = []
        self.res = dict()

    def resolver(self):
        # Validar restricciones y que el problema se pueda resolver con el metodo simplex
        self.validar_restricciones()

        # Contruir Dataframe del problema
        self.tabla_inicial()

        # Contruir las demas tablas hasta el resultado
        self.desarrollar_tablas()

        # Retorna como respuesta el listado de tablas del problema
        self.res["res"] = self.tablas
        self.res["option"] = "M"
        return self.res

    def validar_restricciones(self):
        # Se extrae la matriz de restricciones y se deja por separado el tipo de restricción
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
    
    def tabla_inicial(self):
        # Contruir tabla pandas inicial
        columnas = [f"x{i+1}" for i in range(len(self.coeficientes))] + ["R"]
        tabla = pd.DataFrame(self.numpy_restricciones, columns=columnas)
        tabla.loc[len(tabla)] = np.array(self.coeficientes + [0]) * (-1 if self.objetivo == self.MAXIMIZAR else 1)
        if self.objetivo == self.MINIMIZAR:
            self.objetivo = self.MAXIMIZAR
        tabla.rename(index={len(tabla)-1: f"Z"}, inplace=True)
        # Agregar varibles de holgura a la tabla para los tipo "<=", variables artificiales para los tipo "=" y de exceso y artificial para los tipo ">="
        exceso = 0
        restriccionesM = []
        for r in range(len(self.restricciones)):
            if self.tipo_restricciones[r] == "<=":
                col = [1 if i == r else 0 for i in range(len(self.restricciones))] + [0]
                col = sp.sympify(col)
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", col)
                tabla.rename(index={r: f"S{r+1+exceso}"}, inplace=True)
            elif self.tipo_restricciones[r] == "=":
                col = [1 if i == r else 0 for i in range(len(self.restricciones))] + [self.M if self.objetivo == self.MAXIMIZAR else -self.M]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", col)
                tabla.rename(index={r: f"S{r+1+exceso}"}, inplace=True)
                restriccionesM.append(r)
            elif self.tipo_restricciones[r] == ">=":
                colExceso = [-1 if i == r else 0 for i in range(len(self.restricciones))] + [0]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", colExceso)
                exceso += 1
                col = [1 if i == r else 0 for i in range(len(self.restricciones))] + [self.M if self.objetivo == self.MAXIMIZAR else -self.M]
                tabla.insert(len(tabla.columns)-1, f"S{r+1+exceso}", col)
                tabla.rename(index={r: f"S{r+1+exceso}"}, inplace=True)
                restriccionesM.append(r)
        # Restar variables artificiales con M de la funcion objetivo
        npTabla = tabla.to_numpy()
        for rm in restriccionesM:
            npTabla[-1] -= npTabla[rm] * self.M
        for i in range(len(npTabla)):
            npTabla[i] = sp.sympify(npTabla[i])
        # Nueva tabla inicial
        tabla = pd.DataFrame(npTabla, columns=tabla.columns, index=tabla.index)
        self.tablas.append(tabla)

    def desarrollar_tablas(self):
        while True:
            # Copia la tabla anterior para no modificarla
            tabla_anterior = self.tablas[-1].copy()
            # Verificar Optimalidad
            optimalidad = self.condicion_optimalidad(tabla_anterior)
            if optimalidad:
                self.res["Status"] = "OK"
                return
            # Obtener la columna pivote
            columna_pivote = self.columna_pivote(tabla_anterior)
            # Verificar Factibilidad
            factibilidad = self.condicion_factibilidad(tabla_anterior)
            if not factibilidad:
                self.res["Warning"] = "No Factibilidad: No se puede resolver con el metodo. El problema tiene solución ilimitada no acotada"
                return
            # Obtener la fila pivote
            fila_pivote = self.fila_pivote(tabla_anterior, columna_pivote)
            if not fila_pivote:
                self.res["Warning"] = "Sin Fila Pivote: No se puede resolver con el metodo."
                return
            # Crear nueva tabla
            nueva_tabla = self.crear_nueva_tabla(tabla_anterior, fila_pivote, columna_pivote)
            # Agregar nueva tabla a la lista
            self.tablas.append(nueva_tabla)
        
    def condicion_optimalidad(self, tabla: pd.DataFrame):
        # Se determina si la tabla ha llegado a la condición de optimalidad
        if self.objetivo == self.MAXIMIZAR:
            return np.all([float(i.subs(self.M, self.valueM).evalf()) >= 0 for i in tabla.iloc[-1, :-1]])
        elif self.objetivo == self.MINIMIZAR:
            return np.all([float(i.subs(self.M, self.valueM).evalf()) <= 0 for i in tabla.iloc[-1, :-1]])

    def columna_pivote(self, tabla: pd.DataFrame):
        # Obtiene la columna pivote de la tabla
        if self.objetivo == self.MAXIMIZAR:
            columna = np.argmin([float(i.subs(self.M, self.valueM).evalf()) for i in tabla.iloc[-1, :-1]])
        elif self.objetivo == self.MINIMIZAR:
            columna = np.argmax([float(i.subs(self.M, self.valueM).evalf()) for i in tabla.iloc[-1, :-1]])
        return columna
    
    def condicion_factibilidad(self, tabla: pd.DataFrame):
        # Se determina que al menos uno de sus valores sea mayor que 0
        # En caso contrario se determina que el problema tiene solución ilimitada no acotada
        return np.any([float(i.subs(self.M, self.valueM).evalf()) > 0 for i in tabla.iloc[:-1, -1]])

    def fila_pivote(self, tabla: pd.DataFrame, columna_pivote: str):
        # Obtiene las columnas de R y CP
        R = np.array([float(i.subs(self.M, self.valueM).evalf()) for i in tabla.iloc[:-1]["R"]])
        CP = np.array([float(i.subs(self.M, self.valueM).evalf()) for i in tabla.iloc[:-1, columna_pivote]])
        # Obtiene los resultados de las divisiones
        with np.errstate(divide='ignore', invalid='ignore'):
            operaciones = np.divide(R, CP)
        # Crea una serie de operaciones
        operaciones = pd.Series(operaciones, index=tabla.iloc[:-1].index)
        # Valida que el resultado no sea infinito ni NaN y sea mayor que cero
        validacion = (operaciones != np.inf) & (operaciones != -np.inf) & (operaciones != np.nan) & (operaciones > 0)
        if not operaciones[validacion].empty:
            return operaciones[validacion].idxmin()
        else:
            return False    

    def crear_nueva_tabla(self, tabla: pd.DataFrame, fila_pivote: str, columna_pivote: str):
        nueva_tabla = tabla.copy()
        columna_pivote = nueva_tabla.columns[columna_pivote]
        nueva_tabla.loc[fila_pivote] = tabla.loc[fila_pivote] / tabla.loc[fila_pivote, columna_pivote]
        for i, fila in tabla.iterrows():
            if i != fila_pivote:
                factor_reduccion = tabla.loc[i, columna_pivote] / nueva_tabla.loc[fila_pivote, columna_pivote]
                nueva_tabla.loc[i] = tabla.loc[i] - (nueva_tabla.loc[fila_pivote] * factor_reduccion)
        nueva_tabla = nueva_tabla.rename(index={fila_pivote: columna_pivote})
        return nueva_tabla