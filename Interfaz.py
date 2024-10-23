import tkinter as tk
from tkinter import ttk
import LTI_Dinamica
import LTI_Fuerza_Bruta
import LTI_Voraz

files_content = ["", "", ""]
text_areas = []

def format_process_result(proceso):
    formatted_result = ""
    estado_actual = proceso[0][0]  
    cursor_pos = 0 

    for step in proceso:
        if len(step) == 3:  # Caso Fuerza Bruta (3 valores)
            estado_original, nuevo_estado, accion = step
        else:  # Casos Dinámica y Voraz (2 valores)
            estado_original, accion = step
            nuevo_estado = estado_original  

        if accion == 'advance':
            formatted_result += f"{estado_actual} -> Avanzar\n"
            cursor_pos = min(cursor_pos + 1, len(estado_actual))  

        elif 'replace' in accion:
            original, nuevo = accion.split("'")[1], accion.split("'")[3]
            estado_actual = estado_actual[:cursor_pos] + nuevo + estado_actual[cursor_pos + 1:] 
            formatted_result += f"{estado_actual} -> Reemplazar '{original}' por '{nuevo}'\n"
            cursor_pos += 1  

        elif 'delete' in accion:
            original = accion.split("'")[1]
            estado_actual = estado_actual[:cursor_pos] + estado_actual[cursor_pos + 1:] 
            formatted_result += f"{estado_actual} -> Eliminar '{original}'\n"

        elif 'insert' in accion:
            nuevo = accion.split("'")[1]
            estado_actual = estado_actual[:cursor_pos] + nuevo + estado_actual[cursor_pos:]  
            formatted_result += f"{estado_actual} -> Insertar '{nuevo}'\n"
            cursor_pos += 1  
            
        estado_actual = nuevo_estado
        
    return formatted_result

def replace_word_in_file(tab_index, palabra_original, palabra_nueva):
    if tab_index == 0:
        resultado = LTI_Dinamica.costo_minimo_dinamica(palabra_original, palabra_nueva, 1, 2, 3, 2, 1)
    elif tab_index == 1:
        resultado = LTI_Fuerza_Bruta.costo_minimo_ingenua(palabra_original, palabra_nueva, 1, 2, 3, 2, 1)
    elif tab_index == 2:
        resultado = LTI_Voraz.costo_minimo_voraz(palabra_original, palabra_nueva, 1, 2, 3, 2, 1)

    costo_total = resultado[0]
    proceso = resultado[1]
    return costo_total, format_process_result(proceso)

def on_replace_button_click():
    palabra_original = entry_word_original.get()
    palabra_nueva = entry_word_new.get()
    current_tab = notebook.index(notebook.select())

    if palabra_original and palabra_nueva:
        costo_total, resultado = replace_word_in_file(current_tab, palabra_original, palabra_nueva)

        text_process.delete(1.0, tk.END)
        text_process.insert(tk.END, resultado + '\n')
        text_process.insert(tk.END, f"El costo final de cambiar '{palabra_original}' por '{palabra_nueva}' es de {costo_total}.\n")

root = tk.Tk()
root.title("Reemplazar palabras")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)

notebook.add(tab1, text="Dinámica")
notebook.add(tab2, text="Fuerza Bruta")
notebook.add(tab3, text="Voraz")

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
