def costo_minimo_dinamica(source, target, a, d, r, i, k):
    n, m = len(source), len(target)

    # Inicializar la matriz dp con infinito
    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    operations = [[[] for _ in range(m + 1)] for _ in range(n + 1)]

    # Caso base: transformar una cadena vacía en otra cadena vacía
    dp[0][0] = 0
    operations[0][0] = [(source, "No operation")]

    # Llenar la primera columna (eliminar todos los caracteres de source)
    for x in range(1, n + 1):
        dp[x][0] = dp[x - 1][0] + d
        new_source = source[:x - 1]
        operations[x][0] = operations[x - 1][0] + [(new_source, f"delete '{source[x - 1]}'")]

    # Llenar la primera fila (insertar todos los caracteres de target)
    for y in range(1, m + 1):
        dp[0][y] = dp[0][y - 1] + i
        new_source = operations[0][y - 1][-1][0] + target[y - 1]
        operations[0][y] = operations[0][y - 1] + [(new_source, f"insert '{target[y - 1]}'")]

    # Llenar el resto de la matriz dp
    for x in range(1, n + 1):
        for y in range(1, m + 1):
            # Costo de avanzar o reemplazar
            if source[x - 1] == target[y - 1]:
                cost_advance = dp[x - 1][y - 1] + a
                new_source_advance = operations[x - 1][y - 1][-1][0]
                operation = "advance"
            else:
                cost_replace = dp[x - 1][y - 1] + r
                new_source_replace = operations[x - 1][y - 1][-1][0][:x - 1] + target[y - 1] + operations[x - 1][y - 1][-1][0][x:]
                operation = f"replace '{source[x - 1]}' with '{target[y - 1]}'"

            # Costo de eliminar un carácter
            cost_delete = dp[x - 1][y] + d
            new_source_delete = operations[x - 1][y][-1][0][:x - 1] + operations[x - 1][y][-1][0][x:]

            # Costo de insertar un carácter
            cost_insert = dp[x][y - 1] + i
            new_source_insert = operations[x][y - 1][-1][0][:x] + target[y - 1] + operations[x][y - 1][-1][0][x:]

            # Seleccionar el costo mínimo entre avanzar/reemplazar, eliminar e insertar
            costs = []
            ops = []

            if source[x - 1] == target[y - 1]:
                costs.append(cost_advance)
                ops.append(('advance', new_source_advance))
            else:
                costs.append(cost_replace)
                ops.append((operation, new_source_replace))

            costs.append(cost_delete)
            ops.append((f"delete '{source[x - 1]}'", new_source_delete))

            costs.append(cost_insert)
            ops.append((f"insert '{target[y - 1]}'", new_source_insert))

            # Verificar si hemos alcanzado el final de `target` y sobran caracteres en `source`
            if y == m and x > m:
                cost_kill = dp[x - 1][y] + k
                new_source_kill = target
                costs.append(cost_kill)
                ops.append(('kill', new_source_kill))

            # Determinar el costo mínimo y la operación
            min_cost = min(costs)
            min_index = costs.index(min_cost)
            dp[x][y] = min_cost
            operation, new_source = ops[min_index]

            if operation == 'advance' or "replace" in operation:
                operations[x][y] = operations[x - 1][y - 1] + [(new_source, operation)]
            elif "delete" in operation:
                operations[x][y] = operations[x - 1][y] + [(new_source, operation)]
            elif "insert" in operation:
                operations[x][y] = operations[x][y - 1] + [(new_source, operation)]
            elif operation == 'kill':
                operations[x][y] = operations[x - 1][y] + [(new_source, operation)]
                # Ya aplicamos "kill", podemos retornar
                return dp[x][y], operations[x][y]

    return dp[n][m], operations[n][m]

# Ejemplo de uso
a = 1  # Coste de avanzar
d = 2  # Coste de borrar
r = 3  # Coste de reemplazar
i = 2  # Coste de insertar
k = 1  # Coste de matar

source = "ingeniosossss"
target = "ingeniero"

min_cost, steps = costo_minimo_dinamica(source, target, a, d, r, i, k)

print(f"El costo mínimo para transformar '{source}' en '{target}' es: {min_cost}")
print("\nPasos de la transformación:")
for state, operation in steps:
    print(f"{state:15} -> {operation}")
