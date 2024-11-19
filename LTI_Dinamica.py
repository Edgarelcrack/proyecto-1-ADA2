def costo_minimo_dinamica(source, target, a, d, r, i, k):
    n, m = len(source), len(target)

    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    operations = [[[] for _ in range(m + 1)] for _ in range(n + 1)]
    kill_used = False  

  
    dp[0][0] = 0
    operations[0][0] = [(source, "No operation")]

    for x in range(1, n + 1):
        dp[x][0] = dp[x - 1][0] + d
        new_source = source[:x - 1] 
        operations[x][0] = operations[x - 1][0] + [(new_source, f"delete '{source[x - 1]}'")]

    for y in range(1, m + 1):
        dp[0][y] = dp[0][y - 1] + i
        new_source = operations[0][y - 1][-1][0] + target[y - 1]
        operations[0][y] = operations[0][y - 1] + [(new_source, f"insert '{target[y - 1]}'")]

   
    for x in range(1, n + 1):
        for y in range(1, m + 1):
            if source[x - 1] == target[y - 1]:
                cost_advance = dp[x - 1][y - 1] + a
                new_source_advance = operations[x - 1][y - 1][-1][0][:x - 1] + target[y - 1] + operations[x - 1][y - 1][-1][0][x:]
                operation = "advance"
            else:
                cost_replace = dp[x - 1][y - 1] + r
                new_source_replace = operations[x - 1][y - 1][-1][0][:x - 1] + target[y - 1] + operations[x - 1][y - 1][-1][0][x:]
                operation = f"replace '{source[x - 1]}' with '{target[y - 1]}'"

            cost_delete = dp[x - 1][y] + d
            new_source_delete = operations[x - 1][y][-1][0][:x - 1] + operations[x - 1][y][-1][0][x:]  # Ajustar longitud

            cost_insert = dp[x][y - 1] + i
            new_source_insert = operations[x][y - 1][-1][0][:x] + target[y - 1] + operations[x][y - 1][-1][0][x:]

            costs = [cost_advance if source[x - 1] == target[y - 1] else cost_replace,
                     cost_delete,
                     cost_insert]

            ops = [(operation if source[x - 1] == target[y - 1] else f"replace '{source[x - 1]}' with '{target[y - 1]}'", new_source_advance if source[x - 1] == target[y - 1] else new_source_replace),
                    (f"delete '{source[x - 1]}'", new_source_delete),
                    (f"insert '{target[y - 1]}'", new_source_insert)]

            if y == m and x > m and not kill_used:
                cost_kill = dp[x - 1][y] + k
                new_source_kill = target
                costs.append(cost_kill)
                ops.append(('kill', new_source_kill))
                kill_used = True  

            min_cost = min(costs)
            min_index = costs.index(min_cost)
            dp[x][y] = min_cost
            operation, new_source = ops[min_index]

            if "replace" in operation or operation == 'advance':
                operations[x][y] = operations[x - 1][y - 1] + [(new_source, operation)]
            elif "insert" in operation:
                operations[x][y] = operations[x][y - 1] + [(new_source, operation)]
            else:
                operations[x][y] = operations[x - 1][y] + [(new_source, operation)]

            if new_source == target:
                operations[x][y].append((new_source, "target reached"))
                return dp[x][y], operations[x][y]

    return dp[n][m], operations[n][m]

def imprimir_transformacion(source, steps):
    current_state = list(source)
    print(f"{''.join(current_state):15} -> No operation")
    target_index = 0  

    for step in steps[1:]:
        operation = step[1]
        
        if "delete" in operation:
            char_to_delete = operation.split("'")[1]
            del current_state[target_index]
        
        elif "insert" in operation:
            char_to_insert = operation.split("'")[1]
            current_state.insert(target_index, char_to_insert)
            target_index += 1
        
        elif "replace" in operation:
            new_char = operation.split("'")[3]
            current_state[target_index] = new_char
            target_index += 1  
        
        elif "advance" in operation:
            current_state[target_index] = target[target_index]
            target_index += 1
        
        elif "kill" in operation:
            current_state = list(target)
            target_index = len(target)  
        
        print(f"{''.join(current_state):15} -> {operation}")


a = 1  # avanzar
d = 2  # borrar
r = 3  # reemplazar
i = 2  # insertar
k = 1  # matar

source = "ingeniero"
target = "ingenioso"

min_cost, steps = costo_minimo_dinamica(source, target, a, d, r, i, k)

print(f"El costo mínimo para transformar '{source}' en '{target}' es: {min_cost}")
print("\nPasos de la transformación:")
imprimir_transformacion(source, steps)