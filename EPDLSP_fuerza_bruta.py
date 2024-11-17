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
        ingreso += Acciones_Sobrantes * gobierno[0]  
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

def recopilar_datos():
    A = int(input("Ingrese el total de acciones (A): "))
    B = int(input("Ingrese el precio mínimo por acción (B): "))
    
    NumOferentes = int(input("Ingrese la cantidad de oferentes: "))
    oferentes = []
    
    for i in range(NumOferentes):
        print(f"\nOferente {i + 1}:")
        pi = int(input("  Ingrese el precio por acción (pi): "))
        mi = int(input("  Ingrese el número mínimo de acciones a comprar (mi): "))
        Mi = int(input("  Ingrese el número máximo de acciones a comprar (Mi): "))
        oferentes.append((pi, mi, Mi))
    
    gobierno = (100, 0, 1000)
    return A, B, oferentes, gobierno

A, B, oferentes, gobierno = recopilar_datos()

MejorCombinacion, MaxIngreso = generar_Combinaciones(A, oferentes, B, gobierno)
print(f"\nMejor Combinación: {MejorCombinacion}, Máximo Ingreso: {MaxIngreso}")
            
        
                