import csv

from building import Building
from resident import Resident
from service import Service
from importer import Importer
from utilities import getPath

class Exporter:
    buildingTypes = {}
    occupationTypes = {}
    serviceTypes = {}

    def __init__(self):
        for key, value in Importer.buildingTypes.items():
            Exporter.buildingTypes[value] = key
        
        for key, value in Importer.occupationTypes.items():
            Exporter.occupationTypes[value] = key

        for key, value in Importer.serviceTypes.items():
            Exporter.serviceTypes[value] = key

        self.outputFile = open(getPath("out\\output.txt"), "w")

    def log(self, *args):
        for arg in args:
            self.outputFile.write(str(arg))

    def getWriter(self, file):
        return csv.writer(file, quotechar = '"', quoting = csv.QUOTE_NONNUMERIC, lineterminator = '\n')

    def exportBuildings(self, buildings: list[Building], projectPath):
        with open(getPath(projectPath), "w") as file:
            writer = self.getWriter(file)
            writer.writerows([(building.data.id,
                                building.data.name,
                                Exporter.buildingTypes[building.data.type],
                                building.data.constructionYear,
                                building.data.condition)
            for building in buildings])

    def exportResidents(self, residents: list[Resident], projectPath):
        with open(getPath(projectPath), "w") as file:
            writer = self.getWriter(file)
            writer.writerows([(resident.id,
                                resident.name,
                                resident.birthYear,
                                Exporter.occupationTypes[resident.occupation],
                                resident.residence,
                                resident.happiness)
            for resident in residents])

    def exportServices(self, services: list[Service], projectPath):
        with open(getPath(projectPath), "w") as file:
            writer = self.getWriter(file)
            writer.writerows([(service.id,
                                service.name,
                                Exporter.serviceTypes[service.type],
                                service.affectedBuildings)
            for service in services])
