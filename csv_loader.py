import csv

def load_data(file) -> list[float]:
  with open(file, newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    distribution = []
    for i in reader:
      distribution.append(i)
    assert distribution
    size = len(distribution[0][0])
    process_distribution = [0.0] * (2 ** size)
    for row in distribution:
      index = int(row[0], 2)       
      value = float(row[1])         
      process_distribution[index] = value
  assert int(sum(process_distribution)) == 1 
  return process_distribution, size
