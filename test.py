import pandas as pd
import numpy as np
import sympy as sp


M = sp.symbols("M")
VM = 100000000

a = -5 * M - 8
b = -5 * M - 3
c = -5 * M - 1
d = -5 * M
e = -5 * M + 1
f = -5 * M + 3

tabla = pd.Series([a, b, c, d, e, f], index=["a", "b", "c", "d", "e", "f"])
# print([i.subs(M, VM) >= 0 for i in tabla])

arreglo = np.array([12, 7, 6, 11, np.nan, 9, 1])
print(f"Arreglo original: {arreglo}")

# Crear una máscara para filtrar los elementos NaN y infinitos
mascara = ~np.isnan(arreglo) & ~np.isinf(arreglo)
print(f"Máscara: {mascara}")
# Aplicar la máscara al arreglo
arreglo_filtrado = arreglo[mascara]
print(f"Arreglo filtrado: {arreglo_filtrado}")

# Obtener el índice del elemento menor en el arreglo filtrado
indice_menor_filtrado = np.argmin(arreglo_filtrado)

# Obtener el índice correspondiente en el arreglo original
print(np.where(mascara))
indice_menor = np.where(mascara)[0][indice_menor_filtrado]

print(f"Índice del elemento menor (ignorando NaN e inf): {indice_menor}")
