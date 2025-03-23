from datetime import date
from enum import Enum
from dataclasses import dataclass, field

import moderngl as gl
import pygame as pg

from mesh import Mesh

class BuildingType(Enum):
    Residential = 0
    School = 1
    FireDepartment = 2
    Police = 3
    Hospital = 4
    Office = 5
    CommunityCenter = 6

@dataclass
class BuildingData:
    id: int
    name: str
    type: BuildingType
    constructionDate: date
    usableArea: float
    condition: int

@dataclass
class Building:
    data: BuildingData

    position: pg.Vector3
    rotation: pg.Vector3

class BuildingRenderer:
    def __init__(self):
        self.mesh = Mesh("res\\models\\house.obj", "shaders\\vertexShader.glsl", "shaders\\fragmentShader.glsl")
    
    def updateInstances(self, buildings: list[Building]):
        if len(buildings) == 0:
            return

        instancePositions = [building.position for building in buildings]
        instanceRotations = [building.rotation for building in buildings]
        self.mesh.updateInstances(instancePositions, instanceRotations)

    def draw(self):
        self.mesh.drawInstances()