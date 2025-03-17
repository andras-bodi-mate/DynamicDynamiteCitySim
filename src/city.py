import pygame as pg

from random import random

from building import Building, BuildingType, BuildingRenderer, date
from mesh import Mesh

class City:
    def __init__(self, glContext):
        self.glContext = glContext
        self.buildings: list[Building] = []
        self.buildingRenderer = BuildingRenderer()
        self.roads = []

    def constructBuilding(self):
        position = pg.Vector3(100*random(), 0.0, 100*random())
        rotation = pg.Vector3(0, 0, 0)
        self.buildings.append(Building(self.glContext, 0, "building", BuildingType.Residential, date.today(), 750, position, rotation))

    def draw(self):
        self.buildingRenderer.draw(self.buildings)

        for road in self.roads:
            road.draw()
        
    #def generateBuildings(self):
