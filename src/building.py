from datetime import date
from enum import Enum
from dataclasses import dataclass

import moderngl as gl

from mesh import Mesh
from random import random

class BuildingType(Enum):
    Residential = 0
    School = 1
    HealthService = 2

@dataclass
class Building:
    glContext: gl.Context
    id: int
    name: str
    type: BuildingType
    constructionDate: date
    usableArea: float

    def __post_init__(self):
        self.mesh = Mesh(self.glContext, "res\\models\\house.obj", "shaders\\vertexShader.glsl", "shaders\\fragmentShader.glsl", (random()*50, 0.0, random()*50))

    def draw(self):
        self.mesh.draw()