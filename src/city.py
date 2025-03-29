import moderngl as gl
import glm

from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint, random

from building import Building, BuildingType, BuildingData, BuildingRenderer
from street import Street, StreetRenderer
from intersection import Intersection
from resident import Resident, Occupation
from service import Service, ServiceType
from project import Project, ProjectType
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

        self.currentDate: date = None
        self.endDate: date = None
        self.availableBudget: float = None
        self.hasBeenConfigured = False
        self.minimumHappiness: float = None
        self.residentHappiness: float = None
        self.buildingsCondition: float = None

        self.cityGenerator.generate()
        self.numBuildings = 0

    def constructBuilding(self, buildingData = None):
        newBuilding, newStreetSegments, newIntersections = self.cityGenerator.constructNewBuilding()
        buildingPosition = glm.vec3(10 * newBuilding.pos.x, 0, 10 * newBuilding.pos.y)

        rotation = getRotationFromVector(newBuilding.direction) + 90.0
        if buildingData == None:
            buildingID = Building.getNewID(self.buildings)
            buildingData = BuildingData(buildingID, "Új épület", BuildingType.Residential, self.currentDate, 750)
            for _ in range(2):
                self.residents.append(Resident(Service.getNewID(self.services), "Új lakos", self.currentDate, Occupation.No, buildingID))
        
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

        if self.residentHappiness == None:
            self.residentHappiness = 100.0
        if self.buildingsCondition == None:
            self.buildingsCondition = 100.0

        self.buildingRenderer.updateInstances(self.buildings)
        self.streetRenderer.updateInstances(self.streets)

    def importFilesAndConstruct(self):
        self.importer.openAndImportFiles()
        self.buildings.clear()
        self.residents.clear()
        self.services.clear()
        self.cityGenerator.reset()
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
        self.exporter.exportProjects(self.projects, "out\\VárosfejlesztésiProjektek.csv")

    def updateHappiness(self, newHappiness):
        self.residentHappiness = min(max(0.0, newHappiness), 100.0)

    def updateBuildingsCondition(self, newCondition):
        self.buildingsCondition = min(max(0.0, newCondition), 100.0)

    def updateResidents(self):
        self.updateHappiness(self.residentHappiness - 2.5)
    
    def updateBuildings(self):
        if (randint(1, 10) == 1):
            self.updateBuildingsCondition(self.buildingsCondition - 2)

    def updateProjects(self):
        for project in self.projects:
            if self.currentDate >= project.startDate and self.currentDate <= project.endDate:
                if not project.isActive:
                    print(f"Új projekt kezdődött el: {project.description}")
                    project.isActive = True
            else:
                if project.isActive:
                    print(f"Befefejeződött egy projekt: {project.description}")
                    project.isActive = False
                
                if project.type == ProjectType.ImprovesBuildingConditions:
                    self.updateBuildingsCondition(self.buildingsCondition + 50.0)

                elif project.type == ProjectType.IncreasesResidentHappiness:
                    self.updateHappiness(self.residentHappiness + 50.0)
                else:
                    self.updateBuildingsCondition(self.buildingsCondition + 50.0)
                    self.updateHappiness(self.residentHappiness + 50.0)

            if project.isActive:
                self.availableBudget -= project.monthlyCost

    def updateServices(self):
        for service in self.services:
            if service.newService == False:
                print(f"Egy új szolgáltatás jelent meg: {service.name}")
                service.newService = True
                self.updateHappiness(self.residentHappiness + 30)

    def checkDisasters(self):
        for disaster in Disaster.getDisasters(self.disasters):
            disaster: Disaster
            print(disaster.getNewsHeadline())
            self.updateHappiness(self.residentHappiness + disaster.residentHappinessChange)
            self.updateBuildingsCondition(self.buildingsCondition + disaster.buildingConditionChange)

    def updateToNextMonth(self):
        self.currentDate += relativedelta(months = 1)
        self.updateProjects()
        self.updateBuildings()
        self.updateResidents()
        self.checkDisasters()
        self.exportAllData()
        
        return (self.residentHappiness < self.minimumHappiness or
               self.currentDate > self.endDate or
               self.availableBudget <= 0.0)

    def render(self):
        self.streetRenderer.render()
        self.buildingRenderer.render()
