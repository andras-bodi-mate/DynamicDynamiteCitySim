from importer import Importer

importer = Importer()

importer.openAndImportFiles()

buildings = importer.buildingData
residents = importer.residentData
services = importer.serviceData


print("List of Buildings:")
for building in buildings:
    print(f"ID: {building.id}, Name: {building.name}, Type: {building.buildingType}, "
          f"Construction Date: {building.constructionDate}, Usable Area: {building.usableArea}")


print("\nList of Residents:")
for resident in residents:
    print(f"ID: {resident.id}, Name: {resident.name}, Date of Birth: {resident.dateOfBirth}, "
          f"Occupation: {resident.occupation}, Residence: {resident.residence}")


print("\nList of Services:")
for service in services:
    print(f"ID: {service.id}, Name: {service.name}, Type: {service.serviceType}, "
          f"Affected Buildings: {list(service.affectedBuildings)}")
    
    """
        boldogság számítása:
        előző bodogság/2+((házának állapota/2)-10)+(min(szolgáltatások száma,10))
        (max 50)                  (max 40, min 0)                  (max 10)
    """
def recalchappiness():
    hcondition=0
    numofservices=len(services)
    for resident in residents:
        for building in buildings:
            if building.id==resident.occupation:
                hcondition=building.condition      
        resident.happines=int((resident.happines/2)+(max((hcondition/2)-10,0))+min(numofservices,10))