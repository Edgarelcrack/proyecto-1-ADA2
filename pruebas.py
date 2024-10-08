def costo_minimo_ingenua(source, target, a, d, r, i, k):
    operations = []

    def helper(s, t):
        if not s:
            cost = len(t) * i
            operations.extend([(s, f"insert '{t[j]}'") for j in range(len(t))])
            return cost

        if not t:
            cost = len(s) * d
            operations.extend([(s[:j], f"delete '{s[j]}'") for j in range(len(s))])
            return cost

        if s[0] == t[0]:
            cost = helper(s[1:], t[1:])
            operations.append((s, "advance"))
            return cost + a

        cost_replace = helper(s[1:], t[1:]) + r
        cost_delete = helper(s[1:], t) + d
        cost_insert = helper(s, t[1:]) + i

        min_cost = min(cost_replace, cost_delete, cost_insert)

        if min_cost == cost_replace:
            new_state = s[1:]  # Fuente sin el primer carácter
            operations.append((s, f"replace '{s[0]}' with '{t[0]}'"))
        elif min_cost == cost_delete:
            new_state = s[1:]  # Fuente sin el primer carácter
            operations.append((s, f"delete '{s[0]}'"))
        else:
            new_state = s + t[0]  # Fuente con el primer carácter de destino
            operations.append((s, f"insert '{t[0]}'"))

        return min_cost

    min_cost = helper(source, target)

    return min_cost, operations


# Costos de las operaciones
a = 1  # avanzar
d = 2  # borrar
r = 3  # reemplazar
i = 2  # insertar
k = 1  # matar

source = "ingenioso"
target = "ingeniero"

min_cost, steps = costo_minimo_ingenua(source, target, a, d, r, i, k)

print(f"El costo mínimo para transformar '{source}' en '{target}' es: {min_cost}")
print("\nPasos de la transformación:")
for state, operation in steps:
    print(f"{state:15} -> {operation}")
