from dataclasses import dataclass
from enum import Enum

class ServiceType(Enum):
    HealthCare = 0
    Transportation = 1

@dataclass
class Service:
    id: int
    name: str
    type: ServiceType
    affectedBuildings: list[int]