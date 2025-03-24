from mesh import Mesh

class Street:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

class StreetRenderer:
    def __init__(self):
        self.mesh = Mesh("res\\models\\street.obj", "shaders\\instanceVertexShader.glsl", "shaders\\fragmentShader.glsl",
                         {"Asphalt": "res\\textures\\Asphalt\\asphaltBaseColor.jpg"})
    
    def updateInstances(self, streets: list[Street]):
        if len(streets) == 0:
            return

        instancePositions = [street.position for street in streets]
        instanceRotations = [street.rotation for street in streets]
        self.mesh.updateInstances(instancePositions, instanceRotations)

    def render(self):
        self.mesh.renderInstances()