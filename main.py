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
    for i in range(len(distribution)):
        print(f"{i:0{number_variables}b}: {distribution[i]:.4f}")
    print(f"Suma de probabilidades: {sum(distribution)}")


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
    used_variables = set[int]()
    maskI = get_variables_interest(
        number_variables, number_variables_interest, used_variables
    )
    number_variables_cond = get_number_variables_cond(
        number_variables, number_variables_interest
    )
    maskC, valC = get_variables_cond(
        number_variables, number_variables_cond, used_variables
    )
    maskM = 2**number_variables - 1 ^ maskI ^ maskC
    print(
        f"maskI: {maskI:0{number_variables}b}, "
        f"maskC: {maskC:0{number_variables}b}, "
        f"valC: {valC:0{number_variables}b}, "
        f"maskM: {maskM:0{number_variables}b}"
    )


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
