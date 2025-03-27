from dataclasses import dataclass
from enum import Enum

class Occupation(Enum):
    No = 0
    Student = 1
    Doctor = 2
    Officer = 3
    OfficeWorker = 4
    Teacher = 5
    FireFighter = 6
    Retired = 7
    Mayor = 8

@dataclass
class Resident:
    id: int
    name: str
    birthYear: int
    occupation: Occupation
    residence: int
    happiness: int

    def updateHappiness(self, newHappiness):
        self.happiness = min(max(0.0, newHappiness), 100.0)

    def getNewID(residents):
        return max([resident.id for resident in residents]) + 1 if len(residents) != 0 else 0