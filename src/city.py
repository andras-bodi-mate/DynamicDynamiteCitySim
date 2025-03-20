import pygame as pg

from building import Building, BuildingType, BuildingRenderer, date
from street import Street, StreetRenderer
from intersection import Intersection
from cityGenerator import CityGenerator

class City:
    def __init__(self, glContext):
        self.glContext = glContext
        self.buildings: list[Building] = []
        self.streets: list[Street] = []
        self.intersections: list[Intersection] = []

        self.cityGenerator = CityGenerator(0)
        self.streetRenderer = StreetRenderer()
        self.buildingRenderer = BuildingRenderer()

        self.cityGenerator.generate()
        self.numBuildings = 0

    def constructBuilding(self):
        newBuilding, newStreetSegments, newIntersections = self.cityGenerator.constructNewBuilding()
        buildingPosition = pg.Vector3(10 * newBuilding.pos.x, 0, 10 * newBuilding.pos.y)

        rotation = pg.Vector3(0, 0, 0)
        self.buildings.append(Building(0, "building", BuildingType.Residential, date.today(), 750, buildingPosition, rotation))

        for street in newStreetSegments:
            position = pg.Vector3(10 * street.pos.x, 0, 10 * street.pos.y)
            rotation = 90 if street.isHorizontal else 0
            self.streets.append(Street(position, pg.Vector3(0, rotation, 0)))
        
        for intersection in newIntersections:
            position = pg.Vector3(intersection.pos.x*10, 0, intersection.pos.y*100)
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
            self.intersections.append(Intersection(position, intersection.type, pg.Vector3(0, rotation, 0)))

    def draw(self):
        self.streetRenderer.draw(self.streets)
        self.buildingRenderer.draw(self.buildings)
