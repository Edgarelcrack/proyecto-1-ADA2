def costo_minimo_ingenua(source, target, a, d, r, i, k):
    if not source:
        return len(target) * i, [(source, target[:j], f"insert '{target[j]}'") for j in range(len(target))]

    if not target:
        return len(source) * d, [(source[:j], source[j:], f"delete '{source[j]}'") for j in range(len(source))]

    if source[0] == target[0]:
        cost, operations = costo_minimo_ingenua(source[1:], target[1:], a, d, r, i, k)
        return cost + a, [(source, source, "advance")] + operations

    cost_replace, ops_replace = costo_minimo_ingenua(source[1:], target[1:], a, d, r, i, k)
    cost_replace += r

    cost_delete, ops_delete = costo_minimo_ingenua(source[1:], target, a, d, r, i, k)
    cost_delete += d

    cost_insert, ops_insert = costo_minimo_ingenua(source, target[1:], a, d, r, i, k)
    cost_insert += i

    operations = []

    min_cost = min(cost_replace, cost_delete, cost_insert)
    
    if min_cost == cost_replace:
        new_state = source[0] + target[0] + source[1:]
        operations = [(source, new_state, f"replace '{source[0]}' with '{target[0]}'")] + ops_replace
    elif min_cost == cost_delete:
        new_state = source[1:]
        operations = [(source, new_state, f"delete '{source[0]}'")] + ops_delete
    else:
        new_state = target[0] + source
        operations = [(source, new_state, f"insert '{target[0]}'")] + ops_insert

    return min_cost, operations


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
for original, state, operation in steps:
    print(f"{original:15} -> {operation}")
    
