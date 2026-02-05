import csv

def load_data(fichero):

  with open(fichero, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    distribucion = []
    for i in reader:
      distribucion.append(i)
    if not distribucion:
      raise RuntimeError("empty input file")
    tamaño_entrada = len(distribucion[0][0])
    distribucion_procesada = [0.0] * (2 ** tamaño_entrada)

    for fila in distribucion:
      indice = int(fila[0], 2)       
      valor = float(fila[1])         
      distribucion_procesada[indice] = valor

    print(distribucion_procesada)
