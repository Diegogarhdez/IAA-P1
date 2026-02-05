"""
Generación aleatoria de una distribución conjunta sobre variables binarias.
Valores positivos aleatorios normalizados para que la suma sea 1.
"""

import random


def generate_random_distribution(
    number_random_variables: int,
) -> tuple[list[float], int]:
    """Genera distribución aleatoria. Devuelve (array p normalizado, N)."""
    assert 1 <= number_random_variables <= 64, (
        "Número de variables debe estar entre 1 y 64"
    )
    n_configs = 2**number_random_variables
    distribution = [float(random.randint(1, 100)) for _ in range(n_configs)]
    total = sum(distribution)
    normalized = [x / total for x in distribution]
    return normalized, number_random_variables
