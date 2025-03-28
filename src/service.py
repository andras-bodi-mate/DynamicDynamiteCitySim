from dataclasses import dataclass, field
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
    affectedBuilding: list[int]

    newService: bool = field(default = False, init = False)

    def getNewID(services):
        return max([service.id for service in services]) + 1 if len(services) != 0 else 0