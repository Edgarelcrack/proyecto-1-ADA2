def costo_minimo_voraz(source, target, a, d, r, i, k):
    n, m = len(source), len(target)
    cost = 0
    operations = []

    x, y = 0, 0
    current_state = source
    while x < n and y < m:
        if current_state[x] == target[y]:
            operations.append((current_state, "advance"))
            x += 1
            y += 1
            cost += a
        else:
            # Calcular costos de reemplazar, eliminar e insertar
            cost_replace = r
            cost_delete = d
            cost_insert = i

            # Elegir la operación con el menor costo
            if cost_replace <= cost_delete and cost_replace <= cost_insert:
                current_state = current_state[:x] + target[y] + current_state[x+1:]
                operations.append((current_state, f"replace '{current_state[x]}' with '{target[y]}'"))
                x += 1
                y += 1
                cost += cost_replace
            elif cost_delete <= cost_insert:
                operations.append((current_state[:x] + current_state[x+1:], f"delete '{current_state[x]}'"))
                current_state = current_state[:x] + current_state[x+1:]
                n -= 1  # Ajustar la longitud de la cadena
                cost += cost_delete
            else:
                current_state = current_state[:x] + target[y] + current_state[x:]
                operations.append((current_state, f"insert '{target[y]}'"))
                y += 1
                m += 1  # Ajustar la longitud de la cadena
                cost += cost_insert

    # Eliminar caracteres restantes en `source`
    while x < n:
        operations.append((current_state[:x] + current_state[x+1:], f"delete '{current_state[x]}'"))
        current_state = current_state[:x] + current_state[x+1:]
        x += 1
        cost += d

    # Insertar caracteres restantes en `target`
    while y < m:
        current_state = current_state + target[y]
        operations.append((current_state, f"insert '{target[y]}'"))
        y += 1
        cost += i

    return cost, operations

# Ejemplo de uso
a = 1  # Coste de avanzar
d = 2  # Coste de borrar
r = 3  # Coste de reemplazar
i = 2  # Coste de insertar
k = 1  # Coste de matar

source = "ingeniosossss"
target = "ingeniero"

min_cost, steps = costo_minimo_voraz(source, target, a, d, r, i, k)

print(f"El costo mínimo para transformar '{source}' en '{target}' es: {min_cost}")
print("\nPasos de la transformación:")
for state, operation in steps:
   
    print(f"{state:<15} -> {operation}")