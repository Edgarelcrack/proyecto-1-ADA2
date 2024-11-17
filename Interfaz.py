import tkinter as tk
from tkinter import ttk

import LTI_Dinamica
import LTI_Fuerza_Bruta
import LTI_Voraz
import EPDLSP_dinamica
import EPDLSP_fuerza_bruta
import EPDLSP_voraz

files_content = ["", "", ""]
text_areas = []

def format_process_result(proceso):
    formatted_result = ""
    estado_actual = proceso[0][0]  # Initial state
    
    for step in proceso:
        if len(step) == 3:  # Fuerza Bruta case (3 values)
            estado_original, nuevo_estado, accion = step
            estado_actual = estado_original  # Use original state before applying action
        else:  # Dinámica and Voraz cases (2 values)
            estado_actual, accion = step
            
        # Add the current state before the action
        formatted_result += f"{estado_actual} -> "
        
        # Apply the action and add its description
        if accion == 'advance':
            formatted_result += "Avanzar\n"
            
        elif 'replace' in accion:
            original, nuevo = accion.split("'")[1], accion.split("'")[3]
            formatted_result += f"Reemplazar '{original}' por '{nuevo}'\n"
            
        elif 'delete' in accion:
            original = accion.split("'")[1]
            formatted_result += f"Eliminar '{original}'\n"
            
        elif 'insert' in accion:
            nuevo = accion.split("'")[1]
            formatted_result += f"Insertar '{nuevo}'\n"
            
        elif accion == 'kill':
            formatted_result += "Terminar\n"
            
    return formatted_result

def replace_word_in_file(tab_index, palabra_original, palabra_nueva):
    # Define costs
    costo_avanzar = 1  # a
    costo_borrar = 2   # d
    costo_reemplazar = 3  # r
    costo_insertar = 2  # i
    costo_matar = 1    # k
    
    if tab_index == 0:
        resultado = LTI_Dinamica.costo_minimo_dinamica(
            palabra_original, palabra_nueva, 
            costo_avanzar, costo_borrar, costo_reemplazar, 
            costo_insertar, costo_matar
        )
    elif tab_index == 1:
        resultado = LTI_Fuerza_Bruta.costo_minimo_ingenua(
            palabra_original, palabra_nueva,
            costo_avanzar, costo_borrar, costo_reemplazar,
            costo_insertar, costo_matar
        )
    elif tab_index == 2:
        resultado = LTI_Voraz.costo_minimo_voraz(
            palabra_original, palabra_nueva,
            costo_avanzar, costo_borrar, costo_reemplazar,
            costo_insertar, costo_matar
        )

    costo_total = resultado[0]
    proceso = resultado[1]
    return costo_total, format_process_result(proceso)

def on_replace_button_click():
    palabra_original = entry_word_original.get()
    palabra_nueva = entry_word_new.get()
    current_tab = notebook.index(notebook.select())

    if palabra_original and palabra_nueva:
        costo_total, resultado = replace_word_in_file(current_tab, palabra_original, palabra_nueva)
        
        # Clear previous results
        text_process.delete(1.0, tk.END)
        
        # Show the process and final cost
        text_process.insert(tk.END, resultado)
        text_process.insert(tk.END, f"\nEl costo final de cambiar '{palabra_original}' por '{palabra_nueva}' es de {costo_total}.\n")

root = tk.Tk()
root.title("Reemplazar palabras")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Pestañas principales
tab_LTI = tk.Frame(notebook)
tab_subasta = tk.Frame(notebook)

notebook.add(tab_LTI, text="LTI")
notebook.add(tab_subasta, text="Subasta")

# Subpestañas para LTI
notebook_LTI = ttk.Notebook(tab_LTI)
notebook_LTI.pack(fill='both', expand=True)

tab_dinamica = tk.Frame(notebook_LTI)
tab_fuerza_bruta = tk.Frame(notebook_LTI)
tab_voraz = tk.Frame(notebook_LTI)

notebook_LTI.add(tab_dinamica, text="Dinámica")
notebook_LTI.add(tab_fuerza_bruta, text="Fuerza Bruta")
notebook_LTI.add(tab_voraz, text="Voraz")

# Subpestañas para Subasta
notebook_subasta = ttk.Notebook(tab_subasta)
notebook_subasta.pack(fill='both', expand=True)

tab_subasta_dinamica = tk.Frame(notebook_subasta)
tab_subasta_fuerza_bruta = tk.Frame(notebook_subasta)
tab_subasta_voraz = tk.Frame(notebook_subasta)

notebook_subasta.add(tab_subasta_dinamica, text="Dinámica")
notebook_subasta.add(tab_subasta_fuerza_bruta, text="Fuerza Bruta")
notebook_subasta.add(tab_subasta_voraz, text="Voraz")

# Entradas y botones
label_word_original = tk.Label(root, text="Palabra original:")
label_word_original.pack()

entry_word_original = tk.Entry(root, width=50)
entry_word_original.pack()

label_word_new = tk.Label(root, text="Palabra nueva:")
label_word_new.pack()

entry_word_new = tk.Entry(root, width=50)
entry_word_new.pack()

replace_button = tk.Button(root, text="Reemplazar", command=on_replace_button_click)
replace_button.pack(pady=10)

label_process = tk.Label(root, text="Proceso de reemplazo:")
label_process.pack()

text_process = tk.Text(root, height=10, width=80)
text_process.pack()

root.mainloop()
