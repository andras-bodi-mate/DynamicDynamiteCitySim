import datetime
import glm

from building import Building, BuildingType, BuildingData, BuildingRenderer, date
from street import Street, StreetRenderer
from intersection import Intersection
from cityGenerator import CityGenerator
from importer import Importer
from recalculator import *

class City:
    today=datetime.datetime.now()
    
    dateyear=today.year
    datemonth=today.month
    def __init__(self, glContext):
        self.glContext = glContext
        self.buildings: list[Building] = []
        self.streets: list[Street] = []
        self.intersections: list[Intersection] = []

        self.cityGenerator = CityGenerator(0)
        self.importer = Importer()
        self.streetRenderer = StreetRenderer()
        self.buildingRenderer = BuildingRenderer()

        self.cityGenerator.generate()
        self.numBuildings = 0

    def constructBuilding(self, buildingData = None):
        newBuilding, newStreetSegments, newIntersections = self.cityGenerator.constructNewBuilding()
        buildingPosition = glm.vec3(10 * newBuilding.pos.x, 0, 10 * newBuilding.pos.y)

        rotation = glm.vec3(0, 0, 0)
        if buildingData == None:
            buildingData = BuildingData(0, "building", BuildingType.Residential, date.today(), 750)

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
    def nextMonth(self):
        month=self.datemonth
        year=self.dateyear
        if(month==12):
            month=1
            year+=1
        else:
            month+=1
        self.datemonth=month
        self.dateyear=year
        recalcbuildingcondition()
        recalchappiness(0)
        print(year,month)
    
    def draw(self):
        self.streetRenderer.draw()
        self.buildingRenderer.draw()
