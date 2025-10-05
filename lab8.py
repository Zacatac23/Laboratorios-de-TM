"""
Laboratorio 8 - Análisis de Complejidad Algorítmica
Universidad del Valle de Guatemala
Autor: [Tu Nombre]
Fecha: Octubre 2025
"""

import time
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Tuple

# ==================== EJERCICIO 1 ====================
def ejercicio1(n: int) -> int:
    """
    Complejidad esperada: O(n² log n)
    """
    counter = 0
    i = n // 2
    while i <= n:
        j = 1
        while j + n // 2 <= n:
            k = 1
            while k <= n:
                counter += 1
                k = k * 2
            j += 1
        i += 1
    return counter


# ==================== EJERCICIO 2 ====================
def ejercicio2(n: int) -> int:
    """
    Complejidad esperada: O(n)
    El break en el loop interno hace que solo se ejecute 1 vez por iteración externa
    """
    if n <= 1:
        return 0
    
    counter = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            counter += 1
            break  # Solo ejecuta una vez
    return counter


# ==================== EJERCICIO 3 ====================
def ejercicio3(n: int) -> int:
    """
    Complejidad esperada: O(n²)
    Loop externo: n/3 iteraciones
    Loop interno: n/4 iteraciones
    Total: (n/3) * (n/4) = n²/12 = O(n²)
    """
    counter = 0
    i = 1
    while i <= n // 3:
        j = 1
        while j <= n:
            counter += 1
            j += 4
        i += 1
    return counter


# ==================== FUNCIÓN DE PROFILING ====================
def profile_function(func, input_sizes: List[int]) -> List[Tuple[int, float, int]]:
    """
    Mide el tiempo de ejecución de una función con diferentes tamaños de input.
    
    Args:
        func: Función a perfilar
        input_sizes: Lista de tamaños de input a probar
        
    Returns:
        Lista de tuplas (n, tiempo, operaciones)
    """
    results = []
    
    for n in input_sizes:
        print(f"Probando n = {n:,}...", end=" ")
        
        # Medir tiempo de ejecución
        start_time = time.perf_counter()
        operations = func(n)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        results.append((n, elapsed_time, operations))
        
        print(f"Tiempo: {elapsed_time:.6f}s, Operaciones: {operations:,}")
    
    return results


# ==================== FUNCIÓN PARA CREAR TABLA ====================
def create_table(results: List[Tuple[int, float, int]], exercise_num: int):
    """
    Crea y muestra una tabla con los resultados del profiling.
    """
    df = pd.DataFrame(results, columns=['n', 'Tiempo (s)', 'Operaciones'])
    df['Tiempo (ms)'] = df['Tiempo (s)'] * 1000
    
    print(f"\n{'='*70}")
    print(f"RESULTADOS EJERCICIO {exercise_num}")
    print(f"{'='*70}")
    print(df.to_string(index=False))
    print(f"{'='*70}\n")
    
    return df


# ==================== FUNCIÓN PARA GRAFICAR ====================
def plot_results(results: List[Tuple[int, float, int]], exercise_num: int, complexity: str):
    """
    Crea una gráfica de n vs tiempo de ejecución.
    """
    n_values = [r[0] for r in results]
    times = [r[1] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Tamaño de Input (n)', fontsize=12)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=12)
    plt.title(f'Ejercicio {exercise_num}: Tamaño de Input vs. Tiempo\n'
              f'Complejidad Teórica: {complexity}', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    
    # Añadir anotaciones
    for i, (n, t) in enumerate(zip(n_values, times)):
        plt.annotate(f'{t:.2e}s', 
                    xy=(n, t), 
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'ejercicio_{exercise_num}_grafica.png', dpi=300)
    print(f"Gráfica guardada como: ejercicio_{exercise_num}_grafica.png")
    plt.show()


# ==================== FUNCIÓN PRINCIPAL ====================
def main():
    # Tamaños de input a probar (ajustados según complejidad)
    # Se omiten n=100,000 y n=1,000,000 por tiempos de ejecución prohibitivos
    input_sizes = [1, 10, 100, 1000, 10000]
    
    # Diccionario con ejercicios
    exercises = {
        1: (ejercicio1, "O(n² log n)"),
        2: (ejercicio2, "O(n)"),
        3: (ejercicio3, "O(n²)")
    }
    
    print("="*70)
    print("LABORATORIO 8 - ANÁLISIS DE COMPLEJIDAD ALGORÍTMICA")
    print("Universidad del Valle de Guatemala")
    print("="*70)
    print(f"\nTamaños de input: {input_sizes}")
    print("Nota: Se omiten n=100,000 y n=1,000,000 por tiempos excesivos\n")
    
    # Ejecutar profiling para cada ejercicio
    for ex_num, (func, complexity) in exercises.items():
        print(f"\n{'#'*70}")
        print(f"EJERCICIO {ex_num} - Complejidad: {complexity}")
        print(f"{'#'*70}\n")
        
        results = profile_function(func, input_sizes)
        df = create_table(results, ex_num)
        plot_results(results, ex_num, complexity)
        
        # Guardar resultados en CSV
        csv_filename = f'ejercicio_{ex_num}_resultados.csv'
        df.to_csv(csv_filename, index=False)
        print(f"Resultados guardados en: {csv_filename}\n")
    
    print("="*70)
    print("ANÁLISIS COMPLETO - Todos los ejercicios finalizados")
    print("="*70)


if __name__ == "__main__":
    main()