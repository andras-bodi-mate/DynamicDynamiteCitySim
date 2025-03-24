import glm
import numpy as np
import moderngl as gl

from city import City
from window import Window
from horizon import Horizon
from mesh import Mesh

class Scene:
    def __init__(self, window: Window):
        self.window = window
        self.city = City(window.glContext)
        self.horizon = Horizon("shaders\\horizonVertexShader.glsl", "shaders\\horizonFragmentShader.glsl")
        self.backdrop = Mesh("res\\models\\backdrop.obj", "shaders\\vertexShader.glsl", "shaders\\fragmentShader.glsl",
                             {"Grass": "res\\textures\\Grass\\grassBaseColor.jpg"})
        
    def render(self):
        self.horizon.render()
        self.backdrop.render()
        self.city.render()

    def gameTick(self, deltaTime):
        pass

