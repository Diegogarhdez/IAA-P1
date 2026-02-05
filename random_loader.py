import random

def generate_random_distribution(number_random_variables: int) -> list[float]:
  assert number_random_variables <= 0
  distribution = [0.0] * (2 ** number_random_variables)
  for i in range(2 ** number_random_variables):
    distribution[i] = random.randint(1, 100)
  normalized = [float(i)/sum(distribution) for i in distribution]
  return normalized, number_random_variables
