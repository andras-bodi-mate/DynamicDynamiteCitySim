import moderngl as gl
import glm

from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint, random

from building import Building, BuildingType, BuildingData, BuildingRenderer
from street import Street, StreetRenderer
from intersection import Intersection
from resident import Resident, Occupation
from service import Service
from project import Project
from disaster import Disaster
from cityGenerator import CityGenerator
from importer import Importer
from exporter import Exporter
from utilities import getRotationFromVector, normalisedRandom

class City:
    def __init__(self):
        self.glContext = gl.get_context()
        self.buildings: list[Building] = []
        self.streets: list[Street] = []
        self.intersections: list[Intersection] = []
        self.residents: list[Resident] = []
        self.services: list[Service] = []
        self.projects: list[Project] = []
        self.disasters: list[Disaster] = [
            Disaster("Járvány", 0.01, -30, 0),
            Disaster("Árvíz", 0.03, -20, -30),
            Disaster("Tornádó", 0.02, -30, -30),
            Disaster("Tűzvész", 0.03, -20, -40),
            Disaster("Hurrikán", 0.015, -20, -25)
        ]

        self.cityGenerator = CityGenerator()
        self.importer = Importer()
        self.exporter = Exporter()
        self.streetRenderer = StreetRenderer()
        self.buildingRenderer = BuildingRenderer()

        self.date: date = None
        self.endDate: date = None
        self.availableBudget: float = None
        self.hasBeenConfigured = False
        self.tax = 0.5

        self.cityGenerator.generate()
        self.numBuildings = 0

    def constructBuilding(self, buildingData = None):
        newBuilding, newStreetSegments, newIntersections = self.cityGenerator.constructNewBuilding()
        buildingPosition = glm.vec3(10 * newBuilding.pos.x, 0, 10 * newBuilding.pos.y)

        rotation = getRotationFromVector(newBuilding.direction) + 90.0
        if buildingData == None:
            buildingID = Building.getNewID(self.buildings)
            buildingData = BuildingData(buildingID, "Új épület", BuildingType.Residential, self.date, 750, 100)
            for _ in range(2):
                self.residents.append(Resident(Service.getNewID(self.services), "Új lakos", self.date, Occupation.No, buildingID, 100.0))
        
        buildingPosition += (1.0 + 0.4 * normalisedRandom()) * glm.vec3(newBuilding.direction.x, 0.0, newBuilding.direction.y)
        buildingPosition += 1.25 * normalisedRandom() * glm.vec3(-newBuilding.direction.y, 0.0, newBuilding.direction.x)

        self.buildings.append(Building(buildingData, buildingPosition, glm.vec3(0.0, rotation, 0.0)))

        for street in newStreetSegments:
            position = glm.vec3(10 * street.pos.x, 0, 10 * street.pos.y)
            rotation = 90 if street.isHorizontal else 0
            self.streets.append(Street(position, glm.vec3(0, rotation, 0)))
        
        for intersection in newIntersections:
            position = glm.vec3(intersection.pos.x*10, 0, intersection.pos.y*10)
            rotation = getRotationFromVector(intersection.direction)
            self.intersections.append(Intersection(position, intersection.type, glm.vec3(0, rotation, 0)))

        self.buildingRenderer.updateInstances(self.buildings)
        self.streetRenderer.updateInstances(self.streets)

    def importFilesAndConstruct(self):
        self.importer.openAndImportFiles()
        self.buildings.clear()
        self.residents.clear()
        self.services.clear()
        for buildingData in self.importer.buildingData:
            self.constructBuilding(buildingData)
        
        for resident in self.importer.residentData:
            self.residents.append(resident)

        for service in self.importer.serviceData:
            self.services.append(service)

    def exportAllData(self):
        self.exporter.exportBuildings(self.buildings, "out\\Épületek.csv")
        self.exporter.exportResidents(self.residents, "out\\Lakosok.csv")
        self.exporter.exportServices(self.services, "out\\Szolgáltatások.csv")

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
            occupants = sum((True for resident in self.residents if resident.residence == building.data.id))

            chance = randint(1, 10)
            buildingNewCondition = building.data.condition - occupants

            if (chance == 1):
                buildingNewCondition -= 5

            building.updateCondition(buildingNewCondition)

    def checkDisasters(self):
        for disaster in Disaster.getDisasters(self.disasters):
            print(disaster.getNewsHeadline())
            for resident in self.residents:
                resident.updateHappiness(resident.happiness + disaster.residentHappinessChange)
            
            for building in self.buildings:
                building.updateCondition(building.data.condition + disaster.buildingConditionChange)

    def updateToNextMonth(self):
        self.date += relativedelta(months = 1)
        self.updateBuildings()
        self.updateResidents()
        self.checkDisasters()
        self.exportAllData()
        return self.date < self.endDate

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
