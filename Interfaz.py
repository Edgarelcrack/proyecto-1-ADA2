import tkinter as tk
from tkinter import ttk

# Importar las funciones de los archivos provistos
import LTI_Dinamica
import LTI_Fuerza_Bruta
import LTI_Voraz

# Inicializar contenido de archivos
files_content = ["", "", ""]
text_areas = []

def format_process_result(proceso):
    formatted_result = ""
    estado_actual = proceso[0][0]  # El primer estado de la palabra (estado inicial)
    
    for step in proceso:
        if len(step) == 3:  # Caso de Fuerza Bruta (3 valores)
            estado_original, nuevo_estado, accion = step
        else:  # Otros casos (2 valores)
            estado_original, accion = step
            nuevo_estado = estado_original  # Si no cambia el estado visible, usamos el original

        # Formatear la salida según la acción
        if accion == 'advance':
            formatted_result += f"{estado_original} -> Avanzar\n"
        elif 'replace' in accion:
            original, nuevo = accion.split("'")[1], accion.split("'")[3]
            formatted_result += f"{estado_original} -> Reemplazar '{original}' por '{nuevo}'\n"
        elif 'delete' in accion:
            original = accion.split("'")[1]
            formatted_result += f"{estado_actual} -> Eliminar '{original}'\n"
        elif 'insert' in accion:
            nuevo = accion.split("'")[1]
            formatted_result += f"{estado_actual} -> Insertar '{nuevo}'\n"

        estado_actual = nuevo_estado  # Actualizar el estado actual para la siguiente iteración
    
    return formatted_result




# Función para reemplazar palabra y aplicar la función de los archivos respectivos
def replace_word_in_file(tab_index, palabra_original, palabra_nueva):
    if tab_index == 0:
        # Reemplazo usando la lógica del archivo de Dinámica
        resultado = LTI_Dinamica.costo_minimo_dinamica(palabra_original, palabra_nueva, 1, 2, 3, 2, 1)
    elif tab_index == 1:
        # Reemplazo usando la lógica del archivo de Fuerza Bruta
        resultado = LTI_Fuerza_Bruta.costo_minimo_ingenua(palabra_original, palabra_nueva, 1, 2, 3, 2, 1)
    elif tab_index == 2:
        # Reemplazo usando la lógica del archivo de Voraz
        resultado = LTI_Voraz.costo_minimo_voraz(palabra_original, palabra_nueva, 1, 2, 3, 2, 1)
    
    # El resultado incluye el costo y el proceso, tomamos ambos
    costo_total = resultado[0]  # Costo total
    proceso = resultado[1]      # Proceso paso a paso
    return costo_total, format_process_result(proceso)

# Función para manejar el botón de reemplazo
def on_replace_button_click():
    palabra_original = entry_word_original.get()  # Obtener la palabra original
    palabra_nueva = entry_word_new.get()  # Obtener la palabra nueva
    current_tab = notebook.index(notebook.select())  # Identificar la pestaña actual

    if palabra_original and palabra_nueva:
        # Aplicar el reemplazo y obtener el resultado formateado
        costo_total, resultado = replace_word_in_file(current_tab, palabra_original, palabra_nueva)
        
        # Limpiar cuadro de texto de proceso
        text_process.delete(1.0, tk.END)  
        
        # Mostrar el proceso en el cuadro de texto
        text_process.insert(tk.END, resultado + '\n')
        
        # Mostrar el costo final
        text_process.insert(tk.END, f"El costo final de cambiar '{palabra_original}' por '{palabra_nueva}' es de {costo_total}.\n")

# Configurar ventana principal
root = tk.Tk()
root.title("Reemplazar palabras")

# Crear un notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Crear pestañas
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)

notebook.add(tab1, text="Dinámica")
notebook.add(tab2, text="Fuerza Bruta")
notebook.add(tab3, text="Voraz")

# Zonas de escritura para ingresar las palabras a reemplazar
label_word_original = tk.Label(root, text="Palabra original:")
label_word_original.pack()

entry_word_original = tk.Entry(root, width=50)
entry_word_original.pack()

label_word_new = tk.Label(root, text="Palabra nueva:")
label_word_new.pack()

entry_word_new = tk.Entry(root, width=50)
entry_word_new.pack()

# Botón de reemplazar
replace_button = tk.Button(root, text="Reemplazar", command=on_replace_button_click)
replace_button.pack(pady=10)

# Cuadro de texto para mostrar el proceso
label_process = tk.Label(root, text="Proceso de reemplazo:")
label_process.pack()

text_process = tk.Text(root, height=10, width=80)
text_process.pack()

# Iniciar el loop de la aplicación
root.mainloop()
