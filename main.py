from csv_loader import load_data
from random_loader import generate_random_distribution

def main() -> None:
  name_input_file = input("Nombre del fichero: ") 
  if name_input_file:
    distribution = load_data(name_input_file)
  else:
    number_variables = int(input("Numero de variables a generar: "))
    distribution = generate_random_distribution(number_variables)
  number_varaibles_interest = int(input("Número de variables de interés: "))
  maskI = 0
  for i in range(number_varaibles_interest):
    variable = int(input(f"Variable de interés número {i + 1}"))
    maskI |= variable
  number_varaibles_cond = int(input("Número de variables condicionadas: "))
  maskC = 0
  valC = 0
  for i in range(number_varaibles_cond):
    variable = int(input(f"Variable condicionada número {i + 1}: "))
    maskC |= variable
    value = int(input(f"Valor de la variable {i + 1}: "))
    valC |= value

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