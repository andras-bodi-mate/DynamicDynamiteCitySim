from dataclasses import dataclass, field
from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum

class ProjectType(Enum):
    IncreasesResidentHappiness = 0
    ImprovesBuildingConditions = 1
    Both = 2

@dataclass
class Project:
    id: int
    description: str
    type: ProjectType
    cost: float
    startDate: date
    endDate: date

    isActive: bool = field(default = False, init = False)
    monthlyCost: float = field(default = 0.0, init = False)

    def __post_init__(self):
        relativeTime = relativedelta(self.endDate, self.startDate)
        self.monthlyCost = self.cost / (relativeTime.years * 12 + relativeTime.months)

    def getNewID(services):
        return max([service.id for service in services]) + 1 if len(services) != 0 else 0