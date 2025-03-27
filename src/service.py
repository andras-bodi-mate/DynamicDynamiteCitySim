from dataclasses import dataclass
from enum import Enum

class ServiceType(Enum):
    HealthCare = 0
    Education = 1
    FireDepartment = 2
    Transportation = 3

@dataclass
class Service:
    id: int
    name: str
    type: ServiceType
    affectedBuildings: list[int]

    def getNewID(services):
        return max([service.id for service in services]) + 1 if len(services) != 0 else 0