def subasta(A, B, ofertas):
    ofertas.sort(key=lambda x: x[0], reverse=True)

    acciones_asignadas = [0] * len(ofertas)
    total_valor = 0
    acciones_restantes = A

    for i, (pi, mi, Mi) in enumerate(ofertas):
        acciones_a_asignar = max(mi, min(Mi, acciones_restantes))

        if acciones_restantes >= acciones_a_asignar:
            acciones_asignadas[i] = acciones_a_asignar
            total_valor += acciones_a_asignar * pi
            acciones_restantes -= acciones_a_asignar
        else:
            if acciones_restantes > 0:
                acciones_asignadas[i] = acciones_restantes
                total_valor += acciones_restantes * pi
                acciones_restantes = 0
            break

    if acciones_restantes > 0:
        total_valor += acciones_restantes * B

    return acciones_asignadas, total_valor
