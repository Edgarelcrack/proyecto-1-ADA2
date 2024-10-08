def subasta(A, B, ofertas):
    n = len(ofertas)  
    dp = [[0] * (A + 1) for _ in range(n + 1)]
    asignaciones = [[0] * (A + 1) for _ in range(n + 1)]


    for i in range(1, n + 1):
        pi, mi, Mi = ofertas[i - 1] 
        for a in range(A + 1):
            dp[i][a] = dp[i - 1][a]
            for x in range(mi, min(Mi, a) + 1):
                
                valor_actual = dp[i - 1][a - x] + x * pi
                if valor_actual > dp[i][a]:
                    dp[i][a] = valor_actual
                    asignaciones[i][a] = x

    mejor_valor = dp[n][A] 
    acciones_asignadas = [0] * n
    a = A

   
    for i in range(n, 0, -1):
        acciones_asignadas[i - 1] = asignaciones[i][a]
        a -= asignaciones[i][a]

    return acciones_asignadas, mejor_valor


A = 1000  # Total de acciones
B = 100   # Precio mínimo
ofertas = [
    (500, 0, 600),   
    (450, 100, 400), 
    (400, 100, 400), 
    (200, 50, 200)   
]

asignacion_optima, valor_total = subasta(A, B, ofertas)

print("Asignación óptima:", asignacion_optima)
print("Valor total de la subasta:", valor_total)
