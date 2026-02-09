#!/usr/bin/env python3
"""
Ejemplo de uso del análisis de tiempo de ejecución.
Este script ejecuta un análisis rápido con un número pequeño de variables.
"""

from timing_analyzer import run_timing_analysis, print_results_table, save_results_to_csv, create_visualizations

def main():
    print("\n" + "="*80)
    print("EJEMPLO: Análisis de Tiempo de Ejecución")
    print("="*80)
    
    # Parámetros del análisis
    num_variables = 8  # Número total de variables
    
    print(f"\nEjecutando análisis con {num_variables} variables...")
    print("(Esto tomará aproximadamente 10-20 segundos)\n")
    
    # Ejecutar el análisis
    results = run_timing_analysis(num_variables, num_repetitions=3)
    
    # Mostrar tabla
    print_results_table(results)
    
    # Guardar en CSV
    save_results_to_csv(results, num_variables)
    
    # Crear visualizaciones (si están disponibles)
    print("\nGenerando visualizaciones...")
    create_visualizations(results, num_variables)
    
    print("\n" + "="*80)
    print("Análisis completado exitosamente")
    print("="*80)
    print("\nArchivos generados:")
    print("- timing_results.csv: Datos tabulares")
    print("- timing_results.png: Gráficos (si matplotlib está disponible)")
    print("\nPara un análisis personalizado, ejecuta:")
    print("  python3 timing_analyzer.py")

if __name__ == "__main__":
    main()
