def costo_minimo_ingenua(source, target, a, d, r, i, k):
    if not source:
        return len(target) * i, [(target[:j], f"insert '{target[j]}'") for j in range(len(target))]

    if not target:
        return len(source) * d, [(source[:j], f"delete '{source[j]}'") for j in range(len(source))]

    if source[0] == target[0]:
        cost, operations = costo_minimo_ingenua(source[1:], target[1:], a, d, r, i, k)
        return cost + a, [(source, "advance")] + operations

    cost_replace, ops_replace = costo_minimo_ingenua(source[1:], target[1:], a, d, r, i, k)
    cost_replace += r

    cost_delete, ops_delete = costo_minimo_ingenua(source[1:], target, a, d, r, i, k)
    cost_delete += d

    cost_insert, ops_insert = costo_minimo_ingenua(source, target[1:], a, d, r, i, k)
    cost_insert += i

    min_cost = min(cost_replace, cost_delete, cost_insert)
    operations = []

    if min_cost == cost_replace:
        operations = [(source, f"replace '{source[0]}' with '{target[0]}'")] + ops_replace
    elif min_cost == cost_delete:
        operations = [(source, f"delete '{source[0]}'")] + ops_delete
    else:
        operations = [(source, f"insert '{target[0]}'")] + ops_insert

    return min_cost, operations
