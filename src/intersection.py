from enum import Enum

from mesh import Mesh


class IntersectionType(Enum):
    Three = 0
    Four = 1

class Intersection:
    def __init__(self, position, intersectionType, rotation):
        self.position = position
        self.intersectionType = intersectionType
        self.rotation = rotation

class IntersectionRenderer:
    def __init__(self):
        self.mesh = Mesh("res\\models\\intersection.obj", "shaders\\instanceVertexShader.glsl", "shaders\\fragmentShader.glsl",
                         {"Asphalt": "res\\textures\\Asphalt\\asphaltBaseColor.jpg"})
    
    def updateInstances(self, intersections: list[Intersection]):
        if len(intersections) == 0:
            return

        instancePositions = [intersection.position for intersection in intersections]
        instanceRotations = [intersection.rotation for intersection in intersections]
        self.mesh.updateInstances(instancePositions, instanceRotations)

    def render(self):
        self.mesh.renderInstances()