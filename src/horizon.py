import moderngl as gl
import numpy as np
import glm

from mesh import Mesh
from shader import loadShaders

class Horizon:
    def __init__(self, vertexShaderPath, fragmentShaderPath):
        self.glContext = gl.get_context()
        self.shaderProgram = loadShaders(vertexShaderPath, fragmentShaderPath)
        
        vertices = np.array(
            [-1.0, -1.0,
             -1.0,  1.0,
              1.0, -1.0,
              1.0, -1.0,
             -1.0,  1.0,
              1.0,  1.0],
        dtype = "f4")

        self.vbo = self.glContext.buffer(vertices.tobytes())
        self.vao = self.glContext.vertex_array(self.shaderProgram, self.vbo, "in_vertex")

    def updateUniforms(self, screenSize, fov):
        self.shaderProgram["u_resolution"].write(glm.vec2(screenSize.x, screenSize.y))
        self.shaderProgram["u_fov"].write(glm.vec1(fov))

    def render(self):
        self.vao.render()