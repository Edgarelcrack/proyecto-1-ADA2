from itertools import product

def calcular_valor(asignacion, ofertas, B):
    valor = sum(asignacion[i] * ofertas[i][0] for i in range(len(asignacion))) 
    acciones_sobrantes = A - sum(asignacion)
    valor += acciones_sobrantes * B
    return valor

def asignacion_optima(A, B, ofertas):
    n = len(ofertas) 
    limites = [oferta[2] for oferta in ofertas]
    mejores_asignaciones = []
    mejor_valor = 0

   
    for asignacion in product(*(range(0, Mi + 1) for Mi in limites)):
        if sum(asignacion) <= A:
            valor = calcular_valor(asignacion, ofertas, B)
            if valor > mejor_valor:
                mejor_valor = valor
                mejores_asignaciones = [asignacion]
            elif valor == mejor_valor:
                mejores_asignaciones.append(asignacion)

    return mejores_asignaciones, mejor_valor
o
A = 1000  # Total de acciones
B = 100   # Precio mínimo
ofertas = [
    (500, 0, 600),   
    (450, 100, 400), 
    (400, 100, 400), 
    (200, 50, 200)   
]

asignaciones_optimas, valor_total = asignacion_optima(A, B, ofertas)

print("Asignaciones óptimas:", asignaciones_optimas)
print("Valor total de la subasta:", valor_total)
