from dataclasses import dataclass
from enum import Enum
from datetime import date

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
    dateOfBirth: date
    occupation: Occupation
    residence: int
    happines: int