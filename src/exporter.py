import csv

from building import Building
from resident import Resident
from service import Service
from importer import Importer
from utilities import getPath

class Exporter:
    buildingTypes = {}

    def __init__(self):
        for key, value in Importer.buildingTypes.items():
            Exporter.buildingTypes[value] = key

    def getWriter(self, file):
        return csv.writer(file, quotechar = '"', quoting = csv.QUOTE_NONNUMERIC, lineterminator = '\n')

    def exportBuildings(self, buildings: list[Building], projectPath):
        with open(getPath(projectPath), "w") as file:
            writer = self.getWriter(file)
            writer.writerows([(building.data.id,
                                building.data.name,
                                Exporter.buildingTypes[building.data.type],
                                building.data.constructionDate,
                                building.data.condition)
            for building in buildings])

    def exportResidents(self, buildings: list[Building], projectPath):
        with open(getPath(projectPath), "w") as file:
            writer = self.getWriter(file)
            writer.writerows([(building.data.id,
                                building.data.name,
                                Exporter.buildingTypes[building.data.type],
                                building.data.constructionDate,
                                building.data.condition)
            for building in buildings])