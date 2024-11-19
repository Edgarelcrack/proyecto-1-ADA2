import tkinter as tk
from tkinter import ttk
import LTI_Dinamica
import LTI_Fuerza_Bruta
import LTI_Voraz


def format_process_result(proceso):
    """Formatea los pasos del proceso de transformación para mostrarlos correctamente en la interfaz."""
    formatted_result = ""
    estado_actual = list(proceso[0][0])  # Estado inicial
    cursor_pos = 0  # Posición del cursor

    for step in proceso:
        accion = step[1]

        if "delete" in accion:
            char_to_delete = accion.split("'")[1]
            del estado_actual[cursor_pos]
            formatted_result += f"{''.join(estado_actual):15} -> Eliminar '{char_to_delete}'\n"

        elif "insert" in accion:
            char_to_insert = accion.split("'")[1]
            estado_actual.insert(cursor_pos, char_to_insert)
            formatted_result += f"{''.join(estado_actual):15} -> Insertar '{char_to_insert}'\n"
            cursor_pos += 1  

        elif "replace" in accion:
            original_char = accion.split("'")[1]
            new_char = accion.split("'")[3]
            estado_actual[cursor_pos] = new_char
            formatted_result += f"{''.join(estado_actual):15} -> Reemplazar '{original_char}' por '{new_char}'\n"
            cursor_pos += 1  

        elif "advance" in accion:
            formatted_result += f"{''.join(estado_actual):15} -> Avanzar\n"
            cursor_pos += 1  

        elif "kill" in accion:
            estado_actual = list(step[0])
            formatted_result += f"{''.join(estado_actual):15} -> Matar\n"
            cursor_pos = len(estado_actual)  

    return formatted_result


def replace_word_in_file(tab_index, palabra_original, palabra_nueva):
    """Realiza la transformación de palabras según el algoritmo seleccionado."""
    costs = {
        'advance': 1,
        'delete': 2,
        'replace': 3,
        'insert': 2,
        'kill': 1
    }

    if tab_index == 0:  # Dinámica
        resultado = LTI_Dinamica.costo_minimo_dinamica(
            palabra_original, palabra_nueva, costs['advance'], costs['delete'],
            costs['replace'], costs['insert'], costs['kill']
        )
    elif tab_index == 1:  # Fuerza Bruta
        transformer = LTI_Fuerza_Bruta.WordTransformer(palabra_original, palabra_nueva)
        resultado = transformer.transform()
    elif tab_index == 2:  # Voraz
        transformer = LTI_Voraz.GreedyWordTransformer(palabra_original, palabra_nueva, costs)
        resultado = transformer.transform()

    costo_total, proceso = resultado
    return costo_total, format_process_result(proceso)


def on_replace_button_click():
    """Callback para el botón de reemplazar."""
    palabra_original = entry_word_original.get()
    palabra_nueva = entry_word_new.get()
    current_tab = notebook.index(notebook.select())

    if palabra_original and palabra_nueva:
        try:
            costo_total, resultado = replace_word_in_file(
                current_tab, palabra_original, palabra_nueva
            )

            text_process.delete(1.0, tk.END)
            text_process.insert(tk.END, resultado + '\n')
            text_process.insert(
                tk.END,
                f"El costo final de cambiar '{palabra_original}' por '{palabra_nueva}' es de {costo_total}.\n"
            )
        except Exception as e:
            text_process.delete(1.0, tk.END)
            text_process.insert(tk.END, f"Error: {str(e)}")


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Reemplazar palabras")

# Notebook para las pestañas
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Pestañas para los métodos
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)

notebook.add(tab1, text="Dinámica")
notebook.add(tab2, text="Fuerza Bruta")
notebook.add(tab3, text="Voraz")

# Campos para las palabras original y nueva
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

label_word_original = tk.Label(frame_inputs, text="Palabra original:")
label_word_original.grid(row=0, column=0, padx=5, pady=5)

entry_word_original = tk.Entry(frame_inputs, width=30)
entry_word_original.grid(row=0, column=1, padx=5, pady=5)

label_word_new = tk.Label(frame_inputs, text="Palabra nueva:")
label_word_new.grid(row=1, column=0, padx=5, pady=5)

entry_word_new = tk.Entry(frame_inputs, width=30)
entry_word_new.grid(row=1, column=1, padx=5, pady=5)

# Botón de reemplazo
replace_button = tk.Button(root, text="Reemplazar", command=on_replace_button_click)
replace_button.pack(pady=10)

# Resultado del proceso
label_process = tk.Label(root, text="Proceso de reemplazo:")
label_process.pack()

text_process = tk.Text(root, height=15, width=80)
text_process.pack()

# Ejecutar la interfaz
root.mainloop()
