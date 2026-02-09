"""
Script para generar gráficos a partir de los resultados del análisis de tiempo.
Ejecutar después de haber generado timing_results.csv
"""

import csv
import numpy as np
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Error: matplotlib no está instalado.")
    print("Instala con: pip install matplotlib")
    exit(1)


def load_results_from_csv(csv_file: str) -> dict:
    """Carga los resultados desde un archivo CSV."""
    results = {
        'config': [],
        'num_vars_interest': [],
        'num_vars_cond': [],
        'num_vars_other': [],
        'avg_time': [],
        'min_time': [],
        'max_time': []
    }
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results['config'].append(row['Config'])
            results['num_vars_interest'].append(int(row['Variables_Interes']))
            results['num_vars_cond'].append(int(row['Variables_Condicionadas']))
            results['num_vars_other'].append(int(row['Variables_Otras']))
            results['avg_time'].append(float(row['Tiempo_Promedio_ms']))
            results['min_time'].append(float(row['Tiempo_Min_ms']))
            results['max_time'].append(float(row['Tiempo_Max_ms']))
    
    return results


def create_visualizations(results: dict, number_variables: int) -> None:
    """Crea gráficos para visualizar los resultados."""
    
    # Agrupar resultados por número de variables de interés
    by_interest = {}
    for i in range(len(results['config'])):
        num_interest = results['num_vars_interest'][i]
        if num_interest not in by_interest:
            by_interest[num_interest] = {'cond': [], 'time': [], 'time_other': []}
        by_interest[num_interest]['cond'].append(results['num_vars_cond'][i])
        by_interest[num_interest]['time'].append(results['avg_time'][i])
    
    # Agrupar resultados por número de variables condicionadas
    by_cond = {}
    for i in range(len(results['config'])):
        num_cond = results['num_vars_cond'][i]
        if num_cond not in by_cond:
            by_cond[num_cond] = {'interest': [], 'time': []}
        by_cond[num_cond]['interest'].append(results['num_vars_interest'][i])
        by_cond[num_cond]['time'].append(results['avg_time'][i])
    
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
        heatmap_data[interest_idx, cond_idx] = results['avg_time'][i]
    
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
        configs_grouped[key].append(results['avg_time'][i])
    
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
    plt.savefig('timing_results.png', dpi=150, bbox_inches='tight')
    print("📊 Gráfico guardado en: timing_results.png")
    plt.show()


if __name__ == "__main__":
    csv_file = 'timing_results.csv'
    try:
        results = load_results_from_csv(csv_file)
        # Obtener el número de variables del primer resultado
        num_vars = results['num_vars_interest'][0] + results['num_vars_cond'][0] + results['num_vars_other'][0]
        create_visualizations(results, num_vars)
        print("\n✅ Gráficos generados exitosamente")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {csv_file}")
        print("Ejecuta primero timing_analyzer.py para generar los datos")
