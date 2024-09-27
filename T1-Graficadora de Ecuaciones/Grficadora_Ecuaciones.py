import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# Diccionario con funciones matemáticas permitidas
allowed_functions = {
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'log': np.log,   # Logaritmo natural
    'log10': np.log10,  # Logaritmo en base 10
    'exp': np.exp,
    'sqrt': np.sqrt,
    'abs': np.abs,    # Valor absoluto
    'pi': np.pi,
    'e': np.e,
    'arcsin': np.arcsin,
    'arccos': np.arccos,
    'arctan': np.arctan
}

# Función para generar los campos de entrada de ecuaciones
def crear_campos_ecuaciones():
    try:
        num_ecuaciones = int(num_ecuaciones_entry.get())
        if num_ecuaciones <= 0:
            result_label.config(text="Ingrese un número válido de ecuaciones.")
            return
    except ValueError:
        result_label.config(text="Por favor ingrese un número entero válido.")
        return

    # Limpiar las entradas anteriores
    for widget in ecuaciones_frame.winfo_children():
        widget.destroy()

    # Crear los campos para ingresar ecuaciones
    global ecuaciones_entries
    ecuaciones_entries = []
    for i in range(num_ecuaciones):
        label = tk.Label(ecuaciones_frame, text=f"Ecuación {i + 1}:")
        label.pack(pady=5)
        entry = tk.Entry(ecuaciones_frame, width=50)
        entry.pack(pady=5)
        ecuaciones_entries.append(entry)

# Función para graficar las ecuaciones ingresadas
def graficar_ecuaciones():
    # Obtener las ecuaciones de los campos de entrada
    ecuaciones = [entry.get() for entry in ecuaciones_entries]
    
    # Obtener los valores de los rangos de X
    try:
        x_min = float(x_min_entry.get())
        x_max = float(x_max_entry.get())
        
        if x_min >= x_max:
            result_label.config(text="Error: El valor mínimo de X debe ser menor que el valor máximo.")
            return
    except ValueError:
        result_label.config(text="Error: Ingrese valores numéricos válidos para el rango de X.")
        return
    
    # Definir los valores de x para graficar, según el rango indicado
    x = np.linspace(x_min, x_max, 400)
    
    # Crear una figura para la gráfica
    plt.figure()
    
    # Graficar cada ecuación
    for ecuacion in ecuaciones:
        try:
            # Evaluar la ecuación ingresada con las funciones permitidas
            y = eval(ecuacion, {"__builtins__": None}, {"x": x, **allowed_functions})
            plt.plot(x, y, label=f'y = {ecuacion}')
        except Exception as e:
            result_label.config(text=f"Error al evaluar la ecuación '{ecuacion}': {e}")
            return
    
    # Configurar los límites del eje x
    plt.xlim(x_min, x_max)

    # Añadir líneas en los ejes x = 0 y y = 0
    plt.axhline(0, color='gray', linewidth=2)  # Línea horizontal en y = 0
    plt.axvline(0, color='gray', linewidth=2)  # Línea vertical en x = 0

    # Agregar leyenda y mostrar la gráfica
    plt.legend()
    plt.title("Gráfica de las Ecuaciones")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()
    result_label.config(text="Gráfico generado correctamente.")

# Función para graficar la derivada de la ecuación
def graficar_derivada():
    if not ecuaciones_entries:  # Verifica si hay ecuaciones
        result_label.config(text="No hay ecuaciones ingresadas.")
        return
    
    ecuacion = ecuaciones_entries[0].get()  # Tomamos la primera ecuación para derivar
    try:
        x_sym = sp.Symbol('x')
        ecuacion_sym = sp.sympify(ecuacion, locals=allowed_functions)
        derivada = sp.diff(ecuacion_sym, x_sym)

        # Obtener los valores de los rangos de X
        try:
            x_min = float(x_min_entry.get())
            x_max = float(x_max_entry.get())

            if x_min >= x_max:
                result_label.config(text="Error: El valor mínimo de X debe ser menor que el valor máximo.")
                return
        except ValueError:
            result_label.config(text="Error: Ingrese valores numéricos válidos para el rango de X.")
            return

        # Definir los valores de x para graficar, según el rango indicado
        x = np.linspace(x_min, x_max, 400)
        derivada_num = sp.lambdify(x_sym, derivada, modules=["numpy", {"sqrt": np.sqrt}])
        y_derivada = derivada_num(x)

        # Crear una figura para la gráfica
        plt.figure()
        plt.plot(x, y_derivada, label=f'Derivada de {ecuacion}')
        
        # Configurar los límites del eje x
        plt.xlim(x_min, x_max)

        # Añadir líneas en los ejes x = 0 y y = 0
        plt.axhline(0, color='gray', linewidth=2)  # Línea horizontal en y = 0
        plt.axvline(0, color='gray', linewidth=2)  # Línea vertical en x = 0

        plt.legend()
        plt.title(f'Derivada de {ecuacion}')
        plt.xlabel("x")
        plt.ylabel("y'")
        plt.grid(True)
        plt.show()

        result_label.config(text="Gráfico de la derivada generado correctamente.")
    except Exception as e:
        result_label.config(text=f"Error al calcular la derivada: {e}")

# Función para graficar la integral de la ecuación
def graficar_integral():
    if not ecuaciones_entries:  # Verifica si hay ecuaciones
        result_label.config(text="No hay ecuaciones ingresadas.")
        return
    
    ecuacion = ecuaciones_entries[0].get()  # Tomamos la primera ecuación para integrar
    try:
        x_sym = sp.Symbol('x')
        ecuacion_sym = sp.sympify(ecuacion, locals=allowed_functions)
        integral = sp.integrate(ecuacion_sym, x_sym)

        # Obtener los valores de los rangos de X
        try:
            x_min = float(x_min_entry.get())
            x_max = float(x_max_entry.get())

            if x_min >= x_max:
                result_label.config(text="Error: El valor mínimo de X debe ser menor que el valor máximo.")
                return
        except ValueError:
            result_label.config(text="Error: Ingrese valores numéricos válidos para el rango de X.")
            return

        # Definir los valores de x para graficar, según el rango indicado
        x = np.linspace(x_min, x_max, 400)
        integral_num = sp.lambdify(x_sym, integral, modules=["numpy", {"sqrt": np.sqrt}])
        y_integral = integral_num(x)

        # Crear una figura para la gráfica
        plt.figure()
        plt.plot(x, y_integral, label=f'Integral de {ecuacion}')
        
        # Configurar los límites del eje x
        plt.xlim(x_min, x_max)

        # Añadir líneas en los ejes x = 0 y y = 0
        plt.axhline(0, color='gray', linewidth=2)  # Línea horizontal en y = 0
        plt.axvline(0, color='gray', linewidth=2)  # Línea vertical en x = 0

        plt.legend()
        plt.title(f'Integral de {ecuacion}')
        plt.xlabel("x")
        plt.ylabel("Integral de y")
        plt.grid(True)
        plt.show()

        result_label.config(text="Gráfico de la integral generado correctamente.")
    except Exception as e:
        result_label.config(text=f"Error al calcular la integral: {e}")

# Crear la ventana principal
root = tk.Tk()
root.geometry("600x600")
root.title("Graficadora de Ecuaciones, Derivadas e Integrales")

# Etiqueta y entrada para el número de ecuaciones
num_ecuaciones_label = tk.Label(root, text="¿Cuántas ecuaciones deseas ingresar?")
num_ecuaciones_label.pack(pady=5)

num_ecuaciones_entry = tk.Entry(root, width=5)
num_ecuaciones_entry.pack(pady=5)

# Botón para generar los campos de entrada de ecuaciones
btn_generar_campos = tk.Button(root, text="Generar Campos", command=crear_campos_ecuaciones)
btn_generar_campos.pack(pady=10)

# Frame para las entradas de ecuaciones
ecuaciones_frame = tk.Frame(root)
ecuaciones_frame.pack(pady=10)

# Etiqueta y entradas para el rango de X
x_min_label = tk.Label(root, text="Rango de X (mínimo):")
x_min_label.pack(pady=5)
x_min_entry = tk.Entry(root, width=10)
x_min_entry.pack(pady=5)

x_max_label = tk.Label(root, text="Rango de X (máximo):")
x_max_label.pack(pady=5)
x_max_entry = tk.Entry(root, width=10)
x_max_entry.pack(pady=5)

# Etiqueta para mostrar resultados
result_label = tk.Label(root, text="", fg="red")
result_label.pack(pady=10)

# Botón para graficar las ecuaciones
btn_graficar = tk.Button(root, text="Graficar Ecuaciones", command=graficar_ecuaciones, font=("Arial", 12))
btn_graficar.pack(pady=10)

# Botón para graficar la derivada
btn_derivada = tk.Button(root, text="Graficar Derivada", command=graficar_derivada, font=("Arial", 12))
btn_derivada.pack(pady=10)

# Botón para graficar la integral
btn_integral = tk.Button(root, text="Graficar Integral", command=graficar_integral, font=("Arial", 12))
btn_integral.pack(pady=10)

# Iniciar el loop de la interfaz
root.mainloop()
