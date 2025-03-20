from datetime import date
from enum import Enum
from dataclasses import dataclass, field

import moderngl as gl
import pygame as pg

from mesh import Mesh

class BuildingType(Enum):
    Residential = 0
    School = 1
    HealthService = 2

@dataclass
class Building:
    id: int
    name: str
    type: BuildingType
    constructionDate: date
    usableArea: float

    position: pg.Vector3
    rotation: pg.Vector3

    def __post_init__(self):
        self.glContext = gl.get_context()

class BuildingRenderer:
    def __init__(self):
        self.mesh = Mesh("res\\models\\house.obj", "shaders\\vertexShader.glsl", "shaders\\fragmentShader.glsl")
    
    def draw(self, buildings: list[Building]):
        if len(buildings) == 0:
            return

        instancePositions = [building.position for building in buildings]
        instanceRotations = [building.rotation for building in buildings]
        self.mesh.drawInstanced(instancePositions, instanceRotations)