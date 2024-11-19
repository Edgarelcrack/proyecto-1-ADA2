import tkinter as tk
from tkinter import ttk, messagebox

# Función para imprimir transformación organizada
def imprimir_transformacion(source, steps, target):
    """Genera una salida ordenada para los pasos de transformación."""
    current_state = list(source)
    result = [f"{''.join(current_state):15} -> No operation"]
    target_index = 0

    for step in steps[1:]:
        operation = step[1]

        if "delete" in operation:
            char_to_delete = operation.split("'")[1]
            del current_state[target_index]

        elif "insert" in operation:
            char_to_insert = operation.split("'")[1]
            current_state.insert(target_index, char_to_insert)
            target_index += 1

        elif "replace" in operation:
            new_char = operation.split("'")[3]
            current_state[target_index] = new_char
            target_index += 1

        elif "advance" in operation:
            current_state[target_index] = target[target_index]
            target_index += 1

        elif "kill" in operation:
            current_state = list(target)
            target_index = len(target)

        result.append(f"{''.join(current_state):15} -> {operation}")

    return "\n".join(result)

# Función para ejecutar transformación
def run_transformation():
    """Ejecuta la transformación según el método seleccionado."""
    source = entry_source.get()
    target = entry_target.get()
    method = combo_method.get()

    if not source or not target:
        messagebox.showerror("Error", "Por favor, ingrese ambas palabras.")
        return

    try:
        if method == "Dinámica":
            from LTI_Dinamica import costo_minimo_dinamica
            a, d, r, i, k = 1, 2, 3, 2, 1
            cost, steps = costo_minimo_dinamica(source, target, a, d, r, i, k)
            result_ordered = imprimir_transformacion(source, steps, target)
            result_text.set(f"Costo mínimo: {cost}\nPasos:\n{result_ordered}")

        elif method == "Fuerza Bruta":
            from LTI_Fuerza_Bruta import WordTransformer
            transformer = WordTransformer(source, target)
            cost, steps = transformer.transform()
            result_text.set(f"Costo mínimo: {cost}\nPasos:\n" + "\n".join([f"{word} -> {op}" for word, op in steps]))

        elif method == "Voraz":
            from LTI_Voraz import GreedyWordTransformer
            costs = {'advance': 1, 'delete': 2, 'replace': 3, 'insert': 2, 'kill': 1}
            transformer = GreedyWordTransformer(source, target, costs)
            cost, steps = transformer.transform()
            result_text.set(f"Costo mínimo: {cost}\nPasos:\n" + "\n".join([f"{word} -> {op}" for word, op in steps]))

        else:
            messagebox.showerror("Error", "Seleccione un método válido.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Transformación de Palabras")
root.geometry("600x400")

# Widgets de entrada
frame_input = ttk.Frame(root, padding="10")
frame_input.pack(fill="x", padx=10, pady=10)

ttk.Label(frame_input, text="Palabra Fuente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_source = ttk.Entry(frame_input, width=20)
entry_source.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Palabra Objetivo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_target = ttk.Entry(frame_input, width=20)
entry_target.grid(row=1, column=1, padx=5, pady=5)

# Selector de método
ttk.Label(frame_input, text="Método:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
combo_method = ttk.Combobox(frame_input, values=["Dinámica", "Fuerza Bruta", "Voraz"], state="readonly")
combo_method.grid(row=2, column=1, padx=5, pady=5)
combo_method.current(0)

# Botón para ejecutar
button_run = ttk.Button(frame_input, text="Ejecutar Transformación", command=run_transformation)
button_run.grid(row=3, column=0, columnspan=2, pady=10)

# Área de resultados
frame_results = ttk.Frame(root, padding="10")
frame_results.pack(fill="both", expand=True, padx=10, pady=10)

ttk.Label(frame_results, text="Resultados:").pack(anchor="w")
result_text = tk.StringVar()
result_label = ttk.Label(frame_results, textvariable=result_text, justify="left", wraplength=550)
result_label.pack(anchor="w", fill="both", expand=True)

# Iniciar la aplicación
root.mainloop()
