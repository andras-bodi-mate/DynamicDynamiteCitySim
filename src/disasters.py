from importer import Importer

importer = Importer()

importer.openAndImportFiles()

buildings = importer.buildingData
residents = importer.residentData
services = importer.serviceData


#minden épület -10 condition
def tornado():
    for building in buildings:
        building.condition=max(building.condition-10,0)
        
#minden resident -5 happiness        
def virus():
    for resident in residents:
        resident.happines=max(resident.happines-5,0)