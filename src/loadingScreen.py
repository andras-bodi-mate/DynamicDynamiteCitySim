import moderngl as gl
import numpy as np

from shader import loadShaders
from utilities import getPath

class LoadingScreen:
    def __init__(self, numThingsToBeLoaded, viewport):
        self.glContext = gl.get_context()
        self.shaderProgram = loadShaders("shaders\\loadingBarVertexShader.glsl", "shaders\\loadingBarFragmentShader.glsl")
        self.numThingsToBeLoaded = numThingsToBeLoaded + 1
        self.numLoadedThings = 0

        self.viewport = viewport

        self.barWidth = 1.0
        self.barHeight = 0.1
        self.right = self.barWidth/2
        self.left = -self.barWidth/2
        self.top = self.barHeight/2
        self.bottom = -self.barHeight/2

        outlineVertices = np.array([self.left, self.top, self.right, self.top, self.right, self.bottom, self.left, self.bottom], dtype = "f4")
        outlineIndices = np.array([0, 1, 1, 2, 2, 3, 3, 0], dtype = "i4")
        indices = np.array([0, 1, 3, 1, 2, 3], dtype = "i4")
        self.ibo = self.glContext.buffer(indices.tobytes())
        outlineIbo = self.glContext.buffer(outlineIndices.tobytes())
        vbo = self.glContext.buffer(outlineVertices.tobytes())
        self.outlineVao = self.glContext.vertex_array(self.shaderProgram, vbo, "in_vertex", index_buffer = outlineIbo)

        self.increment(1)

    def increment(self, n = 1):
        self.numLoadedThings += n

        width = self.barWidth * (self.numLoadedThings / self.numThingsToBeLoaded)
        right = self.left + width
        vertices = np.array([self.left, self.top, right, self.top, right, self.bottom, self.left, self.bottom], dtype = "f4")
        vbo = self.glContext.buffer(vertices.tobytes())
        self.vao = self.glContext.vertex_array(self.shaderProgram, vbo, "in_vertex", index_buffer = self.ibo)

        self.glContext.clear()
        self.outlineVao.render(self.glContext.LINES)
        self.vao.render()
        self.viewport.swapBuffers()