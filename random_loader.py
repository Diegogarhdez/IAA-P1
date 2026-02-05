import random
from distribution import Distribution

def generate_random_distribution(number_random_variables: int) -> list[float]:
  if number_random_variables <= 0:
    raise ValueError("invalid number of variables")
  distribution = [0.0] * (2 ** number_random_variables)
  for i in range(2 ** number_random_variables):
    distribution[i] = random.randint(1, 100)
  normalized = [float(i)/sum(distribution) for i in distribution]
  return Distribution(values=normalized, number_variables=number_random_variables)
