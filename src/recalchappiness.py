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