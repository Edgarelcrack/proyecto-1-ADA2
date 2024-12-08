def generar_Combinaciones(A, oferentes, B, gobierno): # A: Cantidad de acciones a vender, oferentes: lista de oferentes, B: Precio de las acciones del gobierno, gobierno: lista con los datos del gobierno
    def Combinacion_Recursiva(OferActual, ActualSuma, ActualCombinacion): #Funcion recursiva para generar las combinaciones
        if ActualSuma == A:# si la suma de las acciones es igual a la cantidad de acciones a vender
            combinations.append(ActualCombinacion[:])  # se almacena la combinacion en la lista de combinaciones
            return
        if OferActual == len(oferentes) or ActualSuma > A: # si se llega al final de la lista de oferentes o la suma de las acciones es mayor a la cantidad de acciones a vender
            return

        min_val = oferentes[OferActual][1] # se obtiene el valor minimo de acciones a comprar
        max_val = oferentes[OferActual][2] # se obtiene el valor maximo de acciones a comprar

        for value in range(min_val, max_val + 1): # se recorre el rango de valores de acciones a comprar    
            if ActualSuma + value <= A:# si la suma de las acciones es menor o igual a la cantidad de acciones a vender
                ActualCombinacion.append(value) # se agrega el valor de acciones a la combinacion actual    
                Combinacion_Recursiva(OferActual + 1, ActualSuma + value, ActualCombinacion) # se llama a la funcion recursiva con el siguiente oferente y la suma de acciones actualizada
                ActualCombinacion.pop() # se elimina el ultimo valor de la combinacion actual

    def calcular_ingreso(combination): #Funcion para calcular el ingreso
        ingreso = 0# se inicializa la variable ingreso en 0
        for i in range(len(combination)):# se recorre la combinacion
            ingreso += combination[i] * oferentes[i][0]# se calcula el ingreso
        Acciones_Sobrantes = A - sum(combination)# se calcula la cantidad de acciones sobrantes  
        ingreso += Acciones_Sobrantes * B # se calcula el ingreso con las acciones sobrantes 
        return ingreso # se retorna el ingreso

    oferentes.append(gobierno) # se agrega el gobierno a la lista de oferentes

    combinations = []# se inicializa la lista de combinaciones
    Combinacion_Recursiva(0, 0, [])# se llama a la funcion recursiva para generar las combinaciones

    ingresos = [calcular_ingreso(combinacion) for combinacion in combinations] # se calcula el ingreso de cada combinacion

    MaxIngreso = 0 # se inicializa el ingreso maximo en 0   
    MejorCombinacion = [] # se inicializa la mejor combinacion en una lista vacia
    for combinacion, ingreso in zip(combinations, ingresos): # se recorren las combinaciones y los ingresos
        if ingreso > MaxIngreso:# si el ingreso es mayor al ingreso maximo
            MaxIngreso = ingreso# se actualiza el ingreso maximo
            MejorCombinacion = combinacion # se actualiza la mejor combinacion

    return MejorCombinacion, MaxIngreso # se retorna la mejor combinacion y el ingreso maximo
                