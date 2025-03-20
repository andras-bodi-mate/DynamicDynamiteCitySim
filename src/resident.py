from dataclasses import dataclass
from enum import Enum
from datetime import date

class Occupation(Enum):
    No = 0
    Student = 1
    Working = 2 #temporary, will change once all occupations are discussed and agreed on.
    Pensioner = 3
@dataclass
class Resident:
    id: int
    name: str
    dateOfBirth: date
    occupation: Occupation
    residence: int