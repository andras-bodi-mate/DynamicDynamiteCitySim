from enum import Enum
from dataclasses import dataclass, field

import glm
import moderngl as gl

from mesh import Mesh

class BuildingType(Enum):
    Residential = 0
    Education = 1
    FireDepartment = 2
    Police = 3
    HealthCare = 4
    Office = 5
    Governmental = 6
    CommunityCenter = 7
    Trade = 8
    Sport = 9
    Transportation = 10

@dataclass
class BuildingData:
    id: int
    name: str
    type: BuildingType
    constructionYear: int
    usableArea: float

@dataclass
class Building:
    data: BuildingData

    position: glm.vec3
    rotation: glm.vec3
    isVisible: bool = field(default = True)

    def getNewID(buildings):
        return max([building.data.id for building in buildings]) + 1 if len(buildings) != 0 else 0

class BuildingRenderer:
    def __init__(self):
        self.mesh = Mesh("res\\models\\house.obj", "shaders\\instanceVertexShader.glsl", "shaders\\fragmentShader.glsl",
                         {"Walnut_Wood": "res\\textures\\Walnut\\walnutBaseColor.jpg",
                          "Red_Brick": "res\\textures\\BrickWall\\brickWallBaseColor.jpeg",
                          "Wood": "res\\textures\\Wood\\woodBaseColor.jpg",
                          "Garage_Door": "res\\textures\\GarageDoor\\garageDoorBaseColor.png",
                          "Metal_Roof": "res\\textures\\Roof\\roofBaseColor.jpg",
                          "Gray_Paint": "res\\textures\\GreyPaint\\greyPaintBaseColor.jpg",
                          "Eggshell_Paint": "res\\textures\\EggshellPaint\\eggshellPaintBaseColor.jpg",
                          "White_Marble_Tiles": "res\\textures\\WhiteMarble\\whiteMarbleBaseColor.jpg",
                          "Black_Metal": "res\\textures\\BlackMetal\\blackMetalBaseColor.jpg"
                          })
    
    def updateInstances(self, buildings: list[Building]):
        if len(buildings) == 0:
            return

        instancePositions = [building.position for building in buildings if building.isVisible]
        instanceRotations = [building.rotation for building in buildings if building.isVisible]
        self.mesh.updateInstances(instancePositions, instanceRotations)

    def render(self):
        self.mesh.renderInstances()