import sys
sys.path.insert(0, '/home/usuario/IAA/IAA-P1')

from timing_analyzer import run_timing_analysis, save_results_to_csv, print_results_table

# Prueba rápida con 4 variables
print("🔄 Ejecutando análisis de timing para 4 variables...")
results = run_timing_analysis(number_variables=4)

print("\n📊 Tabla de resultados:")
print_results_table(results)

print("\n💾 Guardando en CSV...")
save_results_to_csv(results, 4)

print("\n✅ CSV guardado. Verificando decimales...")
with open('timing_results.csv', 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:4]):
        print(f"Línea {i}: {line.rstrip()}")
