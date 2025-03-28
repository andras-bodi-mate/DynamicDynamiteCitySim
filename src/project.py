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

    isActive = False
    monthlyCost: float = field(init = False)

    def __post_init__(self):
        self.monthlyCost = self.cost / relativedelta(self.endDate, self.startDate).months