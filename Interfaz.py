import tkinter as tk
from tkinter import ttk, messagebox

# Funciones para transformación de palabras
def imprimir_transformacion(source, steps, target):
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

def run_transformation():
    source = entry_source.get()
    target = entry_target.get()
    method = combo_method.get()

    if not source or not target:
        messagebox.showerror("Error", "Por favor, ingrese ambas palabras.")
        return

    try:
        if method == "Dinámica":
            from LTI_Dinamica import costo_minimo_dinamica
            cost, steps = costo_minimo_dinamica(source, target, 1, 2, 3, 2, 1)
            result_ordered = imprimir_transformacion(source, steps, target)
            text_result_transform.delete(1.0, tk.END)
            text_result_transform.insert(tk.END, f"Costo mínimo: {cost}\nPasos:\n{result_ordered}")
        elif method == "Fuerza Bruta":
            from LTI_Fuerza_Bruta import WordTransformer
            transformer = WordTransformer(source, target)
            cost, steps = transformer.transform()
            text_result_transform.delete(1.0, tk.END)
            text_result_transform.insert(tk.END, f"Costo mínimo: {cost}\nPasos:\n" + "\n".join([f"{word} -> {op}" for word, op in steps]))
        elif method == "Voraz":
            from LTI_Voraz import GreedyWordTransformer
            costs = {'advance': 1, 'delete': 2, 'replace': 3, 'insert': 2, 'kill': 1}
            transformer = GreedyWordTransformer(source, target, costs)
            cost, steps = transformer.transform()
            text_result_transform.delete(1.0, tk.END)
            text_result_transform.insert(tk.END, f"Costo mínimo: {cost}\nPasos:\n" + "\n".join([f"{word} -> {op}" for word, op in steps]))
        else:
            messagebox.showerror("Error", "Seleccione un método válido.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Funciones para subastas
def agregar_oferentes():
    try:
        num_oferentes = int(entry_oferentes.get())
        for widget in frame_oferentes.winfo_children():
            widget.destroy()
        entries_oferentes.clear()

        for i in range(num_oferentes):
            tk.Label(frame_oferentes, text=f"Oferente {i + 1}:").grid(row=i, column=0, padx=5, pady=5)
            pi_entry = tk.Entry(frame_oferentes, width=10)
            mi_entry = tk.Entry(frame_oferentes, width=10)
            Mi_entry = tk.Entry(frame_oferentes, width=10)
            pi_entry.grid(row=i, column=1, padx=5, pady=5)
            mi_entry.grid(row=i, column=2, padx=5, pady=5)
            Mi_entry.grid(row=i, column=3, padx=5, pady=5)
            entries_oferentes.append((pi_entry, mi_entry, Mi_entry))
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido para la cantidad de oferentes.")

def ejecutar_programa(metodo):
    try:
        total_acciones = int(entry_acciones.get())
        precio_minimo = int(entry_precio.get())

        num_oferentes = int(entry_oferentes.get())
        oferentes = []
        for i in range(num_oferentes):
            pi = int(entries_oferentes[i][0].get())
            mi = int(entries_oferentes[i][1].get())
            Mi = int(entries_oferentes[i][2].get())
            oferentes.append((pi, mi, Mi))

        if metodo == "Dinámica":
            from EPDLSP_dinamica import subasta
            asignacion_optima, valor_total = subasta(total_acciones, precio_minimo, oferentes)
        elif metodo == "Fuerza Bruta":
            from EPDLSP_fuerza_bruta import generar_Combinaciones
            gobierno = (100, 0, 1000)
            asignacion_optima, valor_total = generar_Combinaciones(total_acciones, oferentes, precio_minimo, gobierno)
        elif metodo == "Voraz":
            from EPDLSP_voraz import subasta
            asignacion_optima, valor_total = subasta(total_acciones, precio_minimo, oferentes)
        else:
            raise ValueError("Método no reconocido.")

        text_result_subasta.delete(1.0, tk.END)
        text_result_subasta.insert(tk.END, f"Resultados ({metodo}):\n")
        text_result_subasta.insert(tk.END, f"Asignación óptima: {asignacion_optima}\n")
        text_result_subasta.insert(tk.END, f"Valor total: {valor_total}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error: {str(e)}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Aplicación Unificada")
root.geometry("800x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Pestaña Transformación de Palabras
frame_transform = ttk.Frame(notebook)
notebook.add(frame_transform, text="Transformación de Palabras")

ttk.Label(frame_transform, text="Palabra Fuente:").grid(row=0, column=0, padx=5, pady=5)
entry_source = ttk.Entry(frame_transform)
entry_source.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_transform, text="Palabra Objetivo:").grid(row=1, column=0, padx=5, pady=5)
entry_target = ttk.Entry(frame_transform)
entry_target.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_transform, text="Método:").grid(row=2, column=0, padx=5, pady=5)
combo_method = ttk.Combobox(frame_transform, values=["Dinámica", "Fuerza Bruta", "Voraz"], state="readonly")
combo_method.grid(row=2, column=1, padx=5, pady=5)
combo_method.current(0)

button_transform = ttk.Button(frame_transform, text="Ejecutar Transformación", command=run_transformation)
button_transform.grid(row=3, column=0, columnspan=2, pady=10)

text_result_transform = tk.Text(frame_transform, height=15, width=80)
text_result_transform.grid(row=4, column=0, columnspan=2, pady=5)

# Pestaña Subastas
frame_subasta = ttk.Frame(notebook)
notebook.add(frame_subasta, text="Subastas")

ttk.Label(frame_subasta, text="Total de acciones:").grid(row=0, column=0, padx=5, pady=5)
entry_acciones = ttk.Entry(frame_subasta)
entry_acciones.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_subasta, text="Precio mínimo por acción:").grid(row=1, column=0, padx=5, pady=5)
entry_precio = ttk.Entry(frame_subasta)
entry_precio.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_subasta, text="Número de oferentes:").grid(row=2, column=0, padx=5, pady=5)
entry_oferentes = ttk.Entry(frame_subasta)
entry_oferentes.grid(row=2, column=1, padx=5, pady=5)

button_add_oferentes = ttk.Button(frame_subasta, text="Agregar Oferentes", command=agregar_oferentes)
button_add_oferentes.grid(row=2, column=2, padx=10, pady=5)

frame_oferentes = ttk.Frame(frame_subasta)
frame_oferentes.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
entries_oferentes = []

frame_methods = ttk.Frame(frame_subasta)
frame_methods.grid(row=4, column=0, columnspan=3, pady=10)

button_dinamica = ttk.Button(frame_methods, text="Ejecutar Dinámica", command=lambda: ejecutar_programa("Dinámica"))
button_dinamica.grid(row=0, column=0, padx=10)

button_bruta = ttk.Button(frame_methods, text="Ejecutar Fuerza Bruta", command=lambda: ejecutar_programa("Fuerza Bruta"))
button_bruta.grid(row=0, column=1, padx=10)

button_voraz = ttk.Button(frame_methods, text="Ejecutar Voraz", command=lambda: ejecutar_programa("Voraz"))
button_voraz.grid(row=0, column=2, padx=10)

text_result_subasta = tk.Text(frame_subasta, height=15, width=80)
text_result_subasta.grid(row=5, column=0, columnspan=3, pady=5)

root.mainloop()
