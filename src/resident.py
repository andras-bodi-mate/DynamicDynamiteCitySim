from dataclasses import dataclass
from enum import Enum
from datetime import date

class Occupation(Enum):
    No = 0
    Student = 1
    Worker = 2
    Retired = 3

@dataclass
class Resident:
    id: int
    name: str
    dateOfBirth: date
    occupation: Occupation
    residence: int