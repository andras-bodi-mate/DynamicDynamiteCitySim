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