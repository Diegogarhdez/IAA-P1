"""
Carga de distribución conjunta desde archivo CSV.
Formato: máscara_binaria,probabilidad (ej. 000,0.10)
"""

import csv


def load_csv_distribution(file: str) -> tuple[list[float], int]:
    """Carga distribución desde CSV. Devuelve (array p, número de variables N)."""
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        distribution = [row for row in reader if row]
    assert distribution, "El archivo CSV está vacío"
    size = len(distribution[0][0])
    process_distribution = [0.0] * (2**size)
    for row in distribution:
        index = int(row[0], 2)
        value = float(row[1])
        process_distribution[index] = value
    total = sum(process_distribution)
    assert abs(total - 1.0) < 1e-9, f"La suma de probabilidades debe ser 1, es {total}"
    return process_distribution, size
