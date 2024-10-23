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
            cost_replace = r
            cost_delete = d
            cost_insert = i

            if cost_replace <= cost_delete and cost_replace <= cost_insert:
                current_state = current_state[:x] + target[y] + current_state[x+1:]
                operations.append((current_state, f"replace '{current_state[x]}' with '{target[y]}'"))
                x += 1
                y += 1
                cost += cost_replace
            elif cost_delete <= cost_insert:
                operations.append((current_state[:x] + current_state[x+1:], f"delete '{current_state[x]}'"))
                current_state = current_state[:x] + current_state[x+1:]
                n -= 1 
                cost += cost_delete
            else:
                current_state = current_state[:x] + target[y] + current_state[x:]
                operations.append((current_state, f"insert '{target[y]}'"))
                y += 1
                m += 1  
                cost += cost_insert

    while x < n:
        operations.append((current_state[:x] + current_state[x+1:], f"delete '{current_state[x]}'"))
        current_state = current_state[:x] + current_state[x+1:]
        x += 1
        cost += d

    while y < m:
        current_state = current_state + target[y]
        operations.append((current_state, f"insert '{target[y]}'"))
        y += 1
        cost += i

    return cost, operations
