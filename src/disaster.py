from dataclasses import dataclass
from random import random

@dataclass
class Disaster:
    description: str
    probability: float
    residentHappinessChange: float
    buildingConditionChange: float

    def getDisasters(disasters):
        for disaster in disasters:
            if random() < disaster.probability:
                yield disaster

    def getNewsHeadline(self):
        return (f"Katasztrófa: {self.description}! {self.residentHappinessChange}% boldogság" +
        (f", {self.buildingConditionChange}% épületek állapota" if self.buildingConditionChange != 0 else ""))


#minden épület -10 condition
#def tornado():
#    for building in buildings:
#        building.condition=max(building.condition-10,0)
#        
#minden resident -5 happiness        
#def virus():
#    for resident in residents:
#        resident.happines=max(resident.happines-5,0)