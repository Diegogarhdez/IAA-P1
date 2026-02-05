from dataclasses import dataclass, field

@dataclass
class Distribution:
  values: list[float]
  number_variables: int
