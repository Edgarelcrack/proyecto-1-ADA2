def generar_Combinaciones(A, oferentes, B, gobierno):
    def Combinacion_Recursiva(OferActual, ActualSuma, ActualCombinacion):
        if ActualSuma == A:
            combinations.append(ActualCombinacion[:])
            return
        if OferActual == len(oferentes) or ActualSuma > A:
            return

        min_val = oferentes[OferActual][1]
        max_val = oferentes[OferActual][2]

        for value in range(min_val, max_val + 1):
            if ActualSuma + value <= A:
                ActualCombinacion.append(value)
                Combinacion_Recursiva(OferActual + 1, ActualSuma + value, ActualCombinacion)
                ActualCombinacion.pop()

    def calcular_ingreso(combination):
        ingreso = 0
        for i in range(len(combination)):
            ingreso += combination[i] * oferentes[i][0]
        Acciones_Sobrantes = A - sum(combination)
        ingreso += Acciones_Sobrantes * B
        return ingreso

    oferentes.append(gobierno)

    combinations = []
    Combinacion_Recursiva(0, 0, [])

    ingresos = [calcular_ingreso(combinacion) for combinacion in combinations]

    MaxIngreso = 0
    MejorCombinacion = []
    for combinacion, ingreso in zip(combinations, ingresos):
        if ingreso > MaxIngreso:
            MaxIngreso = ingreso
            MejorCombinacion = combinacion

    return MejorCombinacion, MaxIngreso
                