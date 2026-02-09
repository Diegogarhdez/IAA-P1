"""
Análisis de tiempo de ejecución de la función prob_cond_bin.
Estudia cómo varía el tiempo en función del número de variables de interés
y variables condicionadas.
"""

import time
import itertools
import csv
from random_loader import generate_random_distribution
from main import prob_cond_bin, count_1_bits

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


def generate_mask(variables: list[int], number_variables: int) -> int:
    """Convierte una lista de índices de variables (1-indexados) a una máscara."""
    mask = 0
    for var in variables:
        mask |= 1 << (var - 1)
    return mask


def run_timing_analysis(
    number_variables: int,
    num_repetitions: int = 3
) -> dict:
    """
    Ejecuta análisis de tiempo para prob_cond_bin con diferentes
    combinaciones de variables de interés y condicionadas.
    
    Args:
        number_variables: Número total de variables
        num_repetitions: Número de veces que se repite cada medición (para promediar)
    
    Returns:
        Diccionario con los resultados del análisis
    """
    # Generar distribución aleatoria
    distribution, _ = generate_random_distribution(number_variables)
    
    results = {
        'config': [],
        'num_vars_interest': [],
        'num_vars_cond': [],
        'num_vars_other': [],
        'avg_time': [],
        'min_time': [],
        'max_time': []
    }
    
    # Iterar sobre diferentes números de variables de interés
    for num_interest in range(number_variables + 1):
        available_for_cond = number_variables - num_interest
        
        # Iterar sobre diferentes números de variables condicionadas
        for num_cond in range(available_for_cond + 1):
            num_other = number_variables - num_interest - num_cond
            
            # Generar todas las variables (1, 2, ..., number_variables)
            all_vars = list(range(1, number_variables + 1))
            
            # Generar varias combinaciones para estas cantidades
            num_configs = min(3, 
                            len(list(itertools.combinations(all_vars, num_interest))) if num_interest > 0 else 1)
            
            if num_interest == 0:
                maskI = 0
                interest_configs = [maskI]
            else:
                interest_combos = list(itertools.combinations(all_vars, num_interest))[:num_configs]
                interest_configs = [generate_mask(combo, number_variables) for combo in interest_combos]
            
            for maskI in interest_configs:
                if num_cond == 0:
                    maskC = 0
                    valC = 0
                    cond_configs = [(maskC, valC)]
                else:
                    # Obtener variables no usadas para condicionadas
                    used_in_interest = set()
                    for i in range(number_variables):
                        if (maskI >> i) & 1:
                            used_in_interest.add(i + 1)
                    
                    available_vars = [v for v in all_vars if v not in used_in_interest]
                    cond_combos = list(itertools.combinations(available_vars, num_cond))[:min(3, len(list(itertools.combinations(available_vars, num_cond))))]
                    
                    cond_configs = []
                    for combo in cond_combos:
                        maskC = generate_mask(combo, number_variables)
                        valC = 0  # Usar valor 0 para todas las variables condicionadas
                        cond_configs.append((maskC, valC))
                
                for maskC, valC in cond_configs:
                    # Medir tiempo
                    times = []
                    for _ in range(num_repetitions):
                        start = time.perf_counter()
                        result = prob_cond_bin(distribution, number_variables, maskC, valC, maskI)
                        end = time.perf_counter()
                        if result is not None:
                            times.append(end - start)
                    
                    if times:
                        avg_time = sum(times) / len(times)
                        results['config'].append(
                            f"I={num_interest},C={num_cond},O={num_other}"
                        )
                        results['num_vars_interest'].append(num_interest)
                        results['num_vars_cond'].append(num_cond)
                        results['num_vars_other'].append(num_other)
                        results['avg_time'].append(avg_time)
                        results['min_time'].append(min(times))
                        results['max_time'].append(max(times))
    
    return results


def print_results_table(results: dict) -> None:
    """Imprime los resultados en formato de tabla bonita con colores."""
    # Códigos ANSI para colores
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CYAN = '\033[36m'
    MAGENTA = '\033[35m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    
    total_width = 85
    
    # Encabezado principal con decoración
    print("\n" + CYAN + "╔" + "═" * (total_width - 2) + "╗" + RESET)
    title = " ANÁLISIS DE TIEMPO DE EJECUCIÓN - prob_cond_bin "
    padding = (total_width - len(title)) // 2
    print(CYAN + "║" + RESET + 
          " " * padding + BOLD + title + RESET + 
          " " * (total_width - len(title) - padding - 1) + CYAN + "║" + RESET)
    print(CYAN + "╠" + "═" * (total_width - 2) + "╣" + RESET)
    
    # Encabezados de columnas
    headers = f"{'Config':<12} {'I':<3} {'C':<3} {'O':<3} {'Prom (ms)':<15} {'Mín':<10} {'Máx':<10}"
    print(CYAN + "║" + RESET + f" {BOLD + MAGENTA}{headers}{RESET}" + 
          " " * (total_width - len(headers) - 3) + CYAN + "║" + RESET)
    print(CYAN + "╠" + "═" * (total_width - 2) + "╣" + RESET)
    
    # Datos
    for i in range(len(results['config'])):
        config = results['config'][i]
        num_interest = results['num_vars_interest'][i]
        num_cond = results['num_vars_cond'][i]
        num_other = results['num_vars_other'][i]
        avg_time_ms = results['avg_time'][i] * 1000
        min_time_ms = results['min_time'][i] * 1000
        max_time_ms = results['max_time'][i] * 1000
        
        # Colorear basado en el tiempo
        if avg_time_ms < 0.02:
            time_color = GREEN
            symbol = "▼"
        elif avg_time_ms < 0.1:
            time_color = YELLOW
            symbol = "▬"
        else:
            time_color = MAGENTA
            symbol = "▲"
        
        row = f"{config:<12} {num_interest:<3} {num_cond:<3} {num_other:<3} {time_color}{avg_time_ms:>13.6f}{RESET}  {min_time_ms:>8.4f}  {max_time_ms:>8.4f} {symbol}"
        print(CYAN + "║" + RESET + f" {row}" + 
              " " * (total_width - len(row) - 5) + CYAN + "║" + RESET)
    
    # Pie de tabla
    print(CYAN + "╠" + "═" * (total_width - 2) + "╣" + RESET)
    
    # Estadísticas
    times_ms = [t * 1000 for t in results['avg_time']]
    min_time = min(times_ms)
    max_time = max(times_ms)
    avg_time = sum(times_ms) / len(times_ms)
    
    stats_line = f"Min: {min_time:.6f} | Max: {max_time:.6f} | Prom: {avg_time:.6f} | Total: {len(results['config'])}"
    print(CYAN + "║ " + RESET + f"{GREEN}{BOLD}{stats_line}{RESET}" + 
          " " * (total_width - len(stats_line) - 4) + CYAN + "║" + RESET)
    print(CYAN + "╚" + "═" * (total_width - 2) + "╝" + RESET + "\n")


def create_visualizations(results: dict, number_variables: int) -> None:
    """Crea gráficos para visualizar los resultados."""
    
    if not MATPLOTLIB_AVAILABLE:
        print("\n⚠️  matplotlib no está disponible. Saltando visualización gráfica.")
        print("Para generar gráficos, instala matplotlib: pip install matplotlib")
        return
    
    if not NUMPY_AVAILABLE:
        print("\n⚠️  numpy no está disponible. Saltando visualización gráfica.")
        print("Para generar gráficos, instala numpy: pip install numpy")
        return
    
    # Agrupar resultados por número de variables de interés
    by_interest = {}
    for i in range(len(results['config'])):
        num_interest = results['num_vars_interest'][i]
        if num_interest not in by_interest:
            by_interest[num_interest] = {'cond': [], 'time': [], 'time_other': []}
        by_interest[num_interest]['cond'].append(results['num_vars_cond'][i])
        by_interest[num_interest]['time'].append(results['avg_time'][i] * 1000)  # Convertir a ms
    
    # Agrupar resultados por número de variables condicionadas
    by_cond = {}
    for i in range(len(results['config'])):
        num_cond = results['num_vars_cond'][i]
        if num_cond not in by_cond:
            by_cond[num_cond] = {'interest': [], 'time': []}
        by_cond[num_cond]['interest'].append(results['num_vars_interest'][i])
        by_cond[num_cond]['time'].append(results['avg_time'][i] * 1000)  # Convertir a ms
    
    # Crear figura con múltiples subgráficos
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Análisis de Tiempo de Ejecución - {number_variables} Variables Totales', 
                 fontsize=14, fontweight='bold')
    
    # Gráfico 1: Tiempo promedio vs Número de variables de interés
    ax = axes[0, 0]
    num_interest_vals = sorted(by_interest.keys())
    times_by_interest = [np.mean(by_interest[ni]['time']) for ni in num_interest_vals]
    ax.plot(num_interest_vals, times_by_interest, 'o-', linewidth=2, markersize=8, color='#2E86AB')
    ax.set_xlabel('Número de Variables de Interés', fontsize=11, fontweight='bold')
    ax.set_ylabel('Tiempo Promedio (ms)', fontsize=11, fontweight='bold')
    ax.set_title('Tiempo vs Variables de Interés', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(num_interest_vals)
    
    # Gráfico 2: Tiempo promedio vs Número de variables condicionadas
    ax = axes[0, 1]
    num_cond_vals = sorted(by_cond.keys())
    times_by_cond = [np.mean(by_cond[nc]['time']) for nc in num_cond_vals]
    ax.plot(num_cond_vals, times_by_cond, 's-', linewidth=2, markersize=8, color='#A23B72')
    ax.set_xlabel('Número de Variables Condicionadas', fontsize=11, fontweight='bold')
    ax.set_ylabel('Tiempo Promedio (ms)', fontsize=11, fontweight='bold')
    ax.set_title('Tiempo vs Variables Condicionadas', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(num_cond_vals)
    
    # Gráfico 3: Heatmap de tiempo vs (Variables de interés, Variables condicionadas)
    ax = axes[1, 0]
    unique_interest = sorted(set(results['num_vars_interest']))
    unique_cond = sorted(set(results['num_vars_cond']))
    
    heatmap_data = np.zeros((len(unique_interest), len(unique_cond)))
    for i in range(len(results['config'])):
        interest_idx = unique_interest.index(results['num_vars_interest'][i])
        cond_idx = unique_cond.index(results['num_vars_cond'][i])
        heatmap_data[interest_idx, cond_idx] = results['avg_time'][i] * 1000
    
    im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(len(unique_cond)))
    ax.set_yticks(range(len(unique_interest)))
    ax.set_xticklabels(unique_cond)
    ax.set_yticklabels(unique_interest)
    ax.set_xlabel('Número de Variables Condicionadas', fontsize=11, fontweight='bold')
    ax.set_ylabel('Número de Variables de Interés', fontsize=11, fontweight='bold')
    ax.set_title('Heatmap de Tiempo de Ejecución (ms)', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=ax, label='Tiempo (ms)')
    
    # Gráfico 4: Distribución de tiempos (box plot)
    ax = axes[1, 1]
    configs_grouped = {}
    for i in range(len(results['config'])):
        key = f"I={results['num_vars_interest'][i]},C={results['num_vars_cond'][i]}"
        if key not in configs_grouped:
            configs_grouped[key] = []
        configs_grouped[key].append(results['avg_time'][i] * 1000)
    
    labels = list(configs_grouped.keys())[:12]  # Limitar a 12 para legibilidad
    times_list = [configs_grouped[label] for label in labels]
    
    bp = ax.boxplot(times_list, labels=labels, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#F18F01')
    ax.set_ylabel('Tiempo (ms)', fontsize=11, fontweight='bold')
    ax.set_title('Distribución de Tiempos (primeras 12 configs)', fontsize=12, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('/home/usuario/IAA/IAA-P1/timing_results.png', dpi=150, bbox_inches='tight')
    print("\n📊 Gráfico guardado en: timing_results.png")
    plt.show()


def save_results_to_csv(results: dict, number_variables: int) -> None:
    """Guarda los resultados en un archivo CSV para análisis posterior."""
    csv_file = '/home/usuario/IAA/IAA-P1/timing_results.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Config', 'Variables_Interes', 'Variables_Condicionadas', 
                        'Variables_Otras', 'Tiempo_Promedio_ms', 'Tiempo_Min_ms', 'Tiempo_Max_ms'])
        for i in range(len(results['config'])):
            writer.writerow([
                results['config'][i],
                results['num_vars_interest'][i],
                results['num_vars_cond'][i],
                results['num_vars_other'][i],
                results['avg_time'][i] * 1000,
                results['min_time'][i] * 1000,
                results['max_time'][i] * 1000
            ])
    print(f"\n📊 Datos de resultados guardados en: {csv_file}")


def main_timing_analysis() -> None:
    """Función principal para ejecutar el análisis de tiempo."""
    print("\n" + "="*100)
    print("ANÁLISIS DE TIEMPO DE EJECUCIÓN - prob_cond_bin")
    print("="*100)
    
    while True:
        try:
            num_vars = int(input("\nNúmero de variables para el análisis (recomendado 8-15): "))
            if 1 <= num_vars <= 25:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 25")
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")
    
    print(f"\n⏳ Ejecutando análisis para {num_vars} variables...")
    print("(Esto puede tomar unos segundos...)\n")
    
    results = run_timing_analysis(num_vars, num_repetitions=3)
    
    # Mostrar tabla de resultados
    print_results_table(results)
    
    # Guardar resultados en CSV
    save_results_to_csv(results, num_vars)
    
    # Crear visualizaciones
    print("\n📈 Generando gráficos...")
    create_visualizations(results, num_vars)
    
    print("\n✅ Análisis completado exitosamente")


if __name__ == "__main__":
    main_timing_analysis()
