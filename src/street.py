import pygame as pg

from mesh import Mesh

class Street:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

class StreetRenderer:
    def __init__(self):
        self.mesh = Mesh("res\\models\\street.obj", "shaders\\vertexShader.glsl", "shaders\\fragmentShader.glsl")
    
    def draw(self, streets: list[Street]):
        if len(streets) == 0:
            return

        instancePositions = [building.position for building in streets]
        instanceRotations = [building.rotation for building in streets]
        self.mesh.drawInstanced(instancePositions, instanceRotations)