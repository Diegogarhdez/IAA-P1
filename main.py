import os

from csv_loader import load_csv_distribution
from random_loader import generate_random_distribution


def get_number_variables_interest(number_variables: int) -> int:
    number_variables_interest = int(
        input(f"Número de variables de interés (0-{number_variables}): ")
    )
    while number_variables_interest > number_variables or number_variables_interest < 0:
        print(
            "El número de variables de interés debe ser menor o igual al número de variables"
        )
        number_variables_interest = int(
            input(f"Número de variables de interés (0-{number_variables}): ")
        )
    return number_variables_interest


def get_number_variables_cond(
    number_variables: int, number_variables_interest: int
) -> int:
    available_variables = number_variables - number_variables_interest
    number_variables_cond = int(
        input(f"Número de variables condicionadas (0-{available_variables}): ")
    )
    while number_variables_cond > available_variables or number_variables_cond < 0:
        print(
            "El número de variables condicionadas debe ser menor o igual al número "
            "de variables que quedan después de las de interés",
        )
        number_variables_cond = int(
            input(f"Número de variables condicionadas (0-{available_variables}): ")
        )
    return number_variables_cond


def get_variables_interest(
    number_variables: int, number_variables_interest: int, used_variables: set[int]
) -> int:
    maskI = 0
    for i in range(number_variables_interest):
        variable = int(input(f"Variable de interés número {i + 1}: "))
        while (
            variable > number_variables or variable <= 0 or variable in used_variables
        ):
            print("La variable ya ha sido usada o no es válida, elige otra")
            variable = int(input(f"Variable de interés número {i + 1}: "))
        maskI |= 1 << (variable - 1)
        used_variables.add(variable)
    return maskI


def get_variables_cond(
    number_variables: int, number_variables_cond: int, used_variables: set[int]
) -> tuple[int, int]:
    maskC = 0
    valC = 0
    for i in range(number_variables_cond):
        variable = int(input(f"Variable condicionada número {i + 1}: "))
        while (
            variable > number_variables or variable <= 0 or variable in used_variables
        ):
            print("La variable ya ha sido usada o no es válida, elige otra")
            variable = int(input(f"Variable condicionada número {i + 1}: "))
        maskC |= 1 << (variable - 1)
        used_variables.add(variable)
        value = int(input(f"Valor de la variable X{variable} (0 o 1): "))
        while value not in [0, 1]:
            print("El valor debe ser 0 o 1, elige otra")
            value = int(input(f"Valor de la variable X{variable} (0 o 1): "))
        valC |= value << (variable - 1)
    return maskC, valC


def print_distribution(distribution: list[float], number_variables: int) -> None:
    # Create the header: Xi, Xi-1, ..., X1
    variable_headers = [f"X{number_variables - idx}" for idx in range(number_variables)]
    header = " ".join(variable_headers) + "    P"
    print(header)
    for i in range(len(distribution)):
        bits = f"{i:0{number_variables}b}"
        padded_bits = " ".join(bits)
        print(f"{padded_bits}    {distribution[i]:.4f}")
    print(f"Suma de probabilidades: {sum(distribution)}")


def count_1_bits(mask: int) -> int:
    return bin(mask).count("1")


def _mask_to_index(k: int, maskI: int, number_variables: int) -> int:
    """
    Dada una configuración completa k, devuelve el índice (0 .. 2^|maskI|-1)
    que corresponde a la parte de k en las posiciones donde maskI tiene 1.

    Los bits se toman en orden de posición creciente (bit 0, 1, 2, ...) y se
    escriben en el índice desde el menos significativo: el primer bit de maskI
    va al bit 0 del índice, el siguiente al bit 1, etc.

    Ejemplo: maskI = 0011 (bits 0 y 1), k = 0101 → extraemos bit 0 de k=1,
    bit 1 de k=0 → índice = 01 en binario = 1.
    """
    index = 0
    pos = 0
    for b in range(number_variables):
        if (maskI >> b) & 1:
            index |= ((k >> b) & 1) << pos
            pos += 1
    return index


def prob_cond_bin(
    distribution: list[float], number_variables: int, maskC: int, valC: int, maskI: int
) -> list[float] | None:
    if maskC & maskI:
        return None

    OUTPUT_SIZE = 2 ** count_1_bits(maskI)
    out = [0.0] * OUTPUT_SIZE

    for k in range(len(distribution)):
        if (k & maskC) != valC:
            continue
        idx = _mask_to_index(k, maskI, number_variables)
        out[idx] += distribution[k]

    total = sum(out)
    if total <= 0.0:
        return None

    for i in range(OUTPUT_SIZE):
        out[i] /= total
    return out


def main() -> None:
    name_input_file = input("Nombre del fichero: ")
    if name_input_file:
        while not os.path.exists(name_input_file):
            print("El fichero no existe, elige otro")
            name_input_file = input("Nombre del fichero: ")
        try:
            distribution, number_variables = load_csv_distribution(name_input_file)
        except Exception as e:
            print(f"Error al cargar el fichero: {e}")
            return
    else:
        number_variables = int(input("Numero de variables a generar: "))
        distribution, number_variables = generate_random_distribution(number_variables)
    print_distribution(distribution, number_variables)
    number_variables_interest = get_number_variables_interest(number_variables)
    used_variables: set[int] = set()
    maskI = get_variables_interest(
        number_variables, number_variables_interest, used_variables
    )
    number_variables_cond = get_number_variables_cond(
        number_variables, number_variables_interest
    )
    maskC, valC = get_variables_cond(
        number_variables, number_variables_cond, used_variables
    )
    print(
        f"\nmaskI: {maskI:0{number_variables}b}, "
        f"maskC: {maskC:0{number_variables}b}, "
        f"valC: {valC:0{number_variables}b}, "
    )

    result = prob_cond_bin(distribution, number_variables, maskC, valC, maskI)
    if result is None:
        print(
            "\nNo se puede calcular la distribución condicional (P(X_C)=0 o máscaras solapadas)."
        )
        return

    print("\n--- Distribución condicional P(X_I | X_C) ---")
    countI = count_1_bits(maskI)
    if countI == 0:
        print("  P(∅ | X_C) = 1.000000")
    else:
        bits_I = [b for b in range(number_variables) if (maskI >> b) & 1]
        variable_headers = [f"X{b + 1}" for b in reversed(bits_I)]
        header = " ".join(variable_headers) + "    P"
        print(header)
        for idx in range(len(result)):
            bits_str = " ".join(
                str((idx >> (countI - 1 - j)) & 1) for j in range(countI)
            )
            print(f"{bits_str}    {result[idx]:.6f}")
    print(f"Suma de probabilidades: {sum(result):.6f}")


if __name__ == "__main__":
    main()

# Variables de interes P(ES|TI=sol)
# Preguntas cuantas variables de interes hay => 1. es ES
# Preguntas cuantas variables condicionadas hay => 1. es TI
# Preguntar para cada variable condicionada si su valor es 0 o 1
# Ejemplo
# maskI    maskC    valC
# 00001111 11110000 01100000
# Recorrer con un for 00000000 hasta 00001111
