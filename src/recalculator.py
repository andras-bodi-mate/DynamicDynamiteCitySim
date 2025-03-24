import random
from importer import Importer

importer = Importer()

importer.openAndImportFiles()

buildings = importer.buildingData
residents = importer.residentData
services = importer.serviceData
    
"""
        boldogság számítása:
        ((előző bodogság/2)-10)+((házának állapota/2)-10)+(min(szolgáltatások száma,10))+(10-(adó/10))
        (max 50)                  (max 40, min 0)                  (max 10)
"""
def recalchappiness(tax:int):
    numofservices=len(services)
    for resident in residents:
        for building in buildings:
            if building.id==resident.occupation:
                hcondition=building.condition      
        resident.happines=max(min(int((resident.happines/2)+(max((hcondition/2)-10,0))+min(numofservices,10)+(10-(tax/10))),100),0)
        
        
        
    """
        épület állapotának újraszámolása:
        előzőállapot-lakosok száma +(10% esélyel -5)
    """
    
def recalcbuildingcondition():
    for building in buildings:
        habitants=0
        for resident in residents:
            if(building.id==resident.residence):
                habitants+=1
        chanche=random.randrange(1,10)
        building.condition-=habitants
        if(chanche==1):
            building.condition-=5
        building.condition=max(building.condition,0)