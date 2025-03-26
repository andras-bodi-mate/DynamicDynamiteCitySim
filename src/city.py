import moderngl as gl
import glm

from dateutil.relativedelta import relativedelta
from random import randint

from building import Building, BuildingType, BuildingData, BuildingRenderer, date
from street import Street, StreetRenderer
from intersection import Intersection
from resident import Resident
from service import Service
from cityGenerator import CityGenerator
from importer import Importer
from exporter import Exporter

class City:
    def __init__(self):
        self.glContext = gl.get_context()
        self.buildings: list[Building] = []
        self.streets: list[Street] = []
        self.intersections: list[Intersection] = []
        self.residents: list[Resident] = []
        self.services: list[Service] = []

        self.cityGenerator = CityGenerator()
        self.importer = Importer()
        self.exporter = Exporter()
        self.streetRenderer = StreetRenderer()
        self.buildingRenderer = BuildingRenderer()

        self.date = date.today()
        self.tax = 0.5

        self.cityGenerator.generate()
        self.numBuildings = 0

    def constructBuilding(self, buildingData = None):
        newBuilding, newStreetSegments, newIntersections = self.cityGenerator.constructNewBuilding()
        buildingPosition = glm.vec3(10 * newBuilding.pos.x, 0, 10 * newBuilding.pos.y)

        rotation = glm.vec3(0, 0, 0)
        if buildingData == None:
            buildingData = BuildingData(0, "building", BuildingType.Residential, date.today(), 750, 5)

        self.buildings.append(Building(buildingData, buildingPosition, rotation))

        for street in newStreetSegments:
            position = glm.vec3(10 * street.pos.x, 0, 10 * street.pos.y)
            rotation = 90 if street.isHorizontal else 0
            self.streets.append(Street(position, glm.vec3(0, rotation, 0)))
        
        for intersection in newIntersections:
            position = glm.vec3(intersection.pos.x*10, 0, intersection.pos.y*10)
            if intersection.direction.y == 0:
                if intersection.direction.x > 0:
                    rotation = 270
                else:
                    rotation = 90
            else:
                if intersection.direction.y > 0:
                    rotation = 0
                else:
                    rotation = 180
            self.intersections.append(Intersection(position, intersection.type, glm.vec3(0, rotation, 0)))

        self.buildingRenderer.updateInstances(self.buildings)
        self.streetRenderer.updateInstances(self.streets)

    def importFilesAndConstruct(self):
        self.importer.openAndImportFiles()
        for buildingData in self.importer.buildingData:
            self.constructBuilding(buildingData)

    def exportAllData(self):
        self.exporter.exportBuildings(self.buildings, "out\\Épületek.csv")

    def updateResidents(self):
        numServices = len(self.services)
        for resident in self.residents:
            for building in self.buildings:
                if resident.residence == building.data.id:
                       residenceCondition = building.data.condition
            
            newHappiness = int((resident.happiness/2) + (max((residenceCondition/2) - 10, 0)) + min(numServices, 10) + (10 - (self.tax * 10)))
            resident.updateHappiness(newHappiness)
    
    def updateBuildings(self):
        for building in self.buildings:
            occupants = sum((True for resident in self.residents if resident.residence == building.id))

            chance = randint(1, 10)
            buildingNewCondition = building.data.condition - occupants

            if (chance == 1):
                buildingNewCondition -= 5

            building.updateCondition(buildingNewCondition)

    def updateToNextMonth(self):
        self.date += relativedelta(months = 1)
        self.updateBuildings()
        self.updateResidents()
        self.exportAllData()

    def calculateStatistics(self):
        if len(self.residents) != 0:
            averageResidentHappiness = sum(resident.happiness for resident in self.residents) / len(self.residents)
        else:
            averageResidentHappiness = None

        if len(self.buildings) != 0:
            averageBuildingCondition = sum(building.data.condition for building in self.buildings) / len(self.buildings)
        else:
            averageBuildingCondition = None

        return averageResidentHappiness, averageBuildingCondition

    def render(self):
        self.streetRenderer.render()
        self.buildingRenderer.render()
