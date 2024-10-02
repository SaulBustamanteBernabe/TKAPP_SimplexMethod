import pandas as pd
import numpy as np


class SimplexMethod:

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
        self.simplex_resoluble = None
        self.numpy_coeficientes = None
        self.tablas: list[pd.DataFrame] = []
        self.res = dict()

    def resolver(self):
        # Validar restricciones y que el problema se pueda resolver con el metodo simplex
        self.validar_restricciones()
        if not self.simplex_resoluble:
            return {"Error": "El metodo simplex no es aplicable"}

        # Contruir Dataframe del problema
        self.tabla_inicial()

        # Contruir las demas tablas hasta el resultado
        self.desarrollar_tablas()

        # Retorna como respuesta el listado de tablas del problema
        self.res["res"] = self.tablas
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
        # Se determina si el problema se puede resolver con el metodo simplex
        self.simplex_resoluble = all([tipo == "<=" for tipo in self.tipo_restricciones])
    
    def tabla_inicial(self):
        # Variables de holgura para cada restricción y añadirlos entre las restricciones y resultado
        matriz_var_holgura = np.eye(len(self.restricciones))
        self.numpy_restricciones = np.array(self.numpy_restricciones)
        self.numpy_restricciones = np.concatenate((self.numpy_restricciones[:, :-1], matriz_var_holgura, self.numpy_restricciones[:, -1:]), axis=1)
        # Unir coeficientes de la función Z multiplicados por -1 a la matriz de restricciones
        self.numpy_coeficientes = np.array(self.coeficientes) * -1
        self.numpy_coeficientes = np.concatenate((self.numpy_coeficientes, np.zeros(len(self.restricciones) + 1)))
        tabla1 = np.vstack((self.numpy_restricciones, self.numpy_coeficientes))
        # Crear columnas e indices del dataframe y se guarda como la primera tabla
        columnas = []
        indices = []
        for v in range(len(self.coeficientes)):
            columnas.append(f"x{v+1}")
        for r in range(len(self.restricciones)):
            columnas.append(f"S{r+1}")
            indices.append(f"S{r+1}")
        columnas.append("R")
        indices.append("Z")
        self.tablas.append(pd.DataFrame(tabla1, columns=columnas, index=indices))
    
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
            factibilidad = self.condicion_factibilidad(tabla_anterior, columna_pivote)
            if not factibilidad:
                self.res["Warning"] = "No Factibilidad: No se puede resolver con el metodo simplex. El problema tiene solución ilimitada no acotada"
                return
            # Obtener la fila pivote
            fila_pivote = self.fila_pivote(tabla_anterior, columna_pivote)
            if not fila_pivote:
                self.res["Warning"] = "Sin Fila Pivote: No se puede resolver con el metodo simplex. El problema tiene solución ilimitada no acotada"
                return
            # Crear nueva tabla
            nueva_tabla = self.crear_nueva_tabla(tabla_anterior, fila_pivote, columna_pivote)
            # Agregar nueva tabla a la lista
            self.tablas.append(nueva_tabla)
        


    def condicion_optimalidad(self, tabla: pd.DataFrame):
        # Se determina si la tabla ha llegado a la condición de optimalidad
        if self.objetivo == self.MAXIMIZAR:
            return np.all(tabla.iloc[-1, :-1] >= 0)
        elif self.objetivo == self.MINIMIZAR:
            return np.all(tabla.iloc[-1, :-1] <= 0)

    def columna_pivote(self, tabla: pd.DataFrame):
        # Obtiene la columna pivote de la tabla
        if self.objetivo == self.MAXIMIZAR:
            columna = tabla.iloc[-1, :-1].idxmin()
        elif self.objetivo == self.MINIMIZAR:
            columna = tabla.iloc[-1, :-1].idxmax()
        return columna
    
    def condicion_factibilidad(self, tabla: pd.DataFrame, columna_pivote: str):
        # Se determina que al menos uno de sus valores sea mayor que 0
        # En caso contrario se determina que el problema tiene solución ilimitada no acotada
        return np.any(tabla.iloc[:-1, -1] > 0)

    def fila_pivote(self, tabla: pd.DataFrame, columna_pivote: str):
        # Obtiene la fila pivote de la tabla
        operaciones = tabla.iloc[:-1]["R"] / tabla.iloc[:-1][columna_pivote]
        # Valida que el resultado no sea infinito ni NaN y sea mayor que cero
        validacion = (operaciones != np.inf) & (operaciones != -np.inf) & (operaciones != np.nan) & (operaciones > 0)
        if not operaciones[validacion].empty:
            return operaciones[validacion].idxmin()
        else:
            return False

    def crear_nueva_tabla(self, tabla: pd.DataFrame, fila_pivote: str, columna_pivote: str):
        nueva_tabla = tabla.copy()
        nueva_tabla.loc[fila_pivote] = tabla.loc[fila_pivote] / tabla.loc[fila_pivote, columna_pivote]
        for i, fila in tabla.iterrows():
            if i != fila_pivote:
                factor_reduccion = tabla.loc[i, columna_pivote] / nueva_tabla.loc[fila_pivote, columna_pivote]
                nueva_tabla.loc[i] = tabla.loc[i] - (nueva_tabla.loc[fila_pivote] * factor_reduccion)
        nueva_tabla = nueva_tabla.rename(index={fila_pivote: columna_pivote})
        return nueva_tabla