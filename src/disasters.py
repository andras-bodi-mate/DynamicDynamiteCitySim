from dataclasses import dataclass
from random import random

from city import City

@dataclass
class Disaster:
    probability: float
    residentHappinessChange: float
    buildingConditionChange: float

    def happen(self, city: City):
        for resident in city.residents:
            resident.updateHappiness(resident.updateHappiness + self.residentHappinessChange)
        
        for building in city.buildings:
            building.updateCondition(building.data.condition + self.buildingConditionChange)

    def getDisaster(disasters):
        for disaster in disasters:
            if random() < disaster.probability:
                yield disaster


#minden épület -10 condition
#def tornado():
#    for building in buildings:
#        building.condition=max(building.condition-10,0)
#        
#minden resident -5 happiness        
#def virus():
#    for resident in residents:
#        resident.happines=max(resident.happines-5,0)