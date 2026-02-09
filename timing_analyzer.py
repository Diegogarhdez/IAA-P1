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


def generate_mask(variables: list[int], number_variables: int) -> int:
    """Convierte una lista de índices de variables (1-indexados) a una máscara."""
    # Construir máscara binaria con bits establecidos en posiciones de variables
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
    # === PREPARACIÓN ===
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
    
    # === ITERACIÓN SOBRE COMBINACIONES ===
    for num_interest in range(number_variables + 1):
        available_for_cond = number_variables - num_interest
        
        for num_cond in range(available_for_cond + 1):
            num_other = number_variables - num_interest - num_cond
            all_vars = list(range(1, number_variables + 1))
            
            # === GENERAR COMBINACIONES DE VARIABLES DE INTERÉS ===
            num_configs = min(3, 
                            len(list(itertools.combinations(all_vars, num_interest))) if num_interest > 0 else 1)
            
            if num_interest == 0:
                interest_configs = [0]
            else:
                interest_combos = list(itertools.combinations(all_vars, num_interest))[:num_configs]
                interest_configs = [generate_mask(combo, number_variables) for combo in interest_combos]
            
            for maskI in interest_configs:
                # === GENERAR COMBINACIONES DE VARIABLES CONDICIONADAS ===
                if num_cond == 0:
                    cond_configs = [(0, 0)]
                else:
                    used_in_interest = set()
                    for i in range(number_variables):
                        if (maskI >> i) & 1:
                            used_in_interest.add(i + 1)
                    
                    available_vars = [v for v in all_vars if v not in used_in_interest]
                    cond_combos = list(itertools.combinations(available_vars, num_cond))[:min(3, len(list(itertools.combinations(available_vars, num_cond))))]
                    
                    cond_configs = []
                    for combo in cond_combos:
                        maskC = generate_mask(combo, number_variables)
                        valC = 0
                        cond_configs.append((maskC, valC))
                
                for maskC, valC in cond_configs:
                    # === MEDIR TIEMPO DE EJECUCIÓN ===
                    times = []
                    for _ in range(num_repetitions):
                        start = time.perf_counter()
                        result = prob_cond_bin(distribution, number_variables, maskC, valC, maskI)
                        end = time.perf_counter()
                        if result is not None:
                            times.append(end - start)
                    
                    # === ALMACENAR RESULTADOS ===
                    if times:
                        avg_time = sum(times) / len(times)
                        results['config'].append(f"I={num_interest},C={num_cond},O={num_other}")
                        results['num_vars_interest'].append(num_interest)
                        results['num_vars_cond'].append(num_cond)
                        results['num_vars_other'].append(num_other)
                        results['avg_time'].append(avg_time)
                        results['min_time'].append(min(times))
                        results['max_time'].append(max(times))
    
    return results


def print_results_table(results: dict) -> None:
    """Imprime los resultados en formato de tabla bonita con colores."""
    # === DEFINICIÓN DE COLORES ANSI ===
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CYAN = '\033[36m'
    MAGENTA = '\033[35m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    total_width = 85
    
    # === ENCABEZADO ===
    print("\n" + CYAN + "╔" + "═" * (total_width - 2) + "╗" + RESET)
    title = " ANÁLISIS DE TIEMPO DE EJECUCIÓN"
    padding = (total_width - len(title)) // 2
    print(CYAN + "║" + RESET + 
          " " * padding + BOLD + title + RESET + 
          " " * (total_width - len(title) - padding - 1) + CYAN + "║" + RESET)
    print(CYAN + "╠" + "═" * (total_width - 2) + "╣" + RESET)
    
    # === COLUMNAS ===
    headers = f"{'Config':<12} {'I':<3} {'C':<3} {'O':<3} {'Prom (ms)':<10} {'Mín':<7} {'Máx':<7}"
    print(CYAN + "║" + RESET + f" {BOLD + MAGENTA}{headers}{RESET}" + 
          " " * (total_width - len(headers) - 3) + CYAN + "║" + RESET)
    print(CYAN + "╠" + "═" * (total_width - 2) + "╣" + RESET)
    
    # === DATOS ===
    for i in range(len(results['config'])):
        config = results['config'][i]
        num_interest = results['num_vars_interest'][i]
        num_cond = results['num_vars_cond'][i]
        num_other = results['num_vars_other'][i]
        avg_time_ms = results['avg_time'][i] * 1000
        min_time_ms = results['min_time'][i] * 1000
        max_time_ms = results['max_time'][i] * 1000
        
        # Asignar color y símbolo según velocidad de ejecución
        if avg_time_ms < 0.02:
            time_color = GREEN
            symbol = "▼"
        elif avg_time_ms < 0.1:
            time_color = YELLOW
            symbol = "▬"
        else:
            time_color = MAGENTA
            symbol = "▲"
        
        row = f"{config:<12} {num_interest:<3} {num_cond:<3} {num_other:<3} {time_color}{avg_time_ms:>9.4f}{RESET}  {min_time_ms:>6.4f}  {max_time_ms:>6.4f} {symbol}"
        print(CYAN + "║" + RESET + f" {row}" + 
              " " * (total_width - len(row) - 5) + CYAN + "║" + RESET)
    
    # === PIE CON ESTADÍSTICAS ===
    print(CYAN + "╠" + "═" * (total_width - 2) + "╣" + RESET)
    times_ms = [t * 1000 for t in results['avg_time']]
    stats_line = f"Min: {min(times_ms):.4f} | Max: {max(times_ms):.4f} | Prom: {sum(times_ms)/len(times_ms):.4f} | Total: {len(results['config'])}"
    print(CYAN + "║ " + RESET + f"{GREEN}{BOLD}{stats_line}{RESET}" + 
          " " * (total_width - len(stats_line) - 4) + CYAN + "║" + RESET)
    print(CYAN + "╚" + "═" * (total_width - 2) + "╝" + RESET + "\n")





def save_results_to_csv(results: dict, number_variables: int) -> None:
    """Guarda los resultados en un archivo CSV para análisis posterior."""
    csv_file = '/home/usuario/IAA/IAA-P1/timing_results.csv'
    
    # === ESCRIBIR CSV ===
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
                f"{results['avg_time'][i] * 1000:.4f}",
                f"{results['min_time'][i] * 1000:.4f}",
                f"{results['max_time'][i] * 1000:.4f}"
            ])
    print(f"\n📊 Datos de resultados guardados en: {csv_file}")


def main_timing_analysis() -> None:
    """Función principal para ejecutar el análisis de tiempo."""
    print("\n" + "="*100)
    print("ANÁLISIS DE TIEMPO DE EJECUCIÓN")
    print("="*100)
    
    # === ENTRADA DE USUARIO ===
    while True:
        try:
            num_vars = int(input("\nNúmero de variables para el análisis (recomendado 8-15): "))
            if 1 <= num_vars <= 32:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 32")
        except ValueError:
            print("Entrada inválida. Ingresa un número entero.")
    
    # === EJECUTAR ANÁLISIS ===
    print(f"\n⏳ Ejecutando análisis para {num_vars} variables...")
    print("(Esto puede tomar unos segundos...)\n")
    results = run_timing_analysis(num_vars, num_repetitions=3)
    
    # === GENERAR REPORTES ===
    print_results_table(results)
    save_results_to_csv(results, num_vars)
    print("\n✅ Análisis completado exitosamente")


if __name__ == "__main__":
    main_timing_analysis()
