import pyobjloader
import numpy as np

from pathHandler import getPath
from shader import loadShaders

class Mesh:
    def __init__(self, glContext, modelPath, vertexShaderPath, fragmentShaderPath, position = (0.0, 0.0, 0.0)):
        self.shaderProgram = loadShaders(glContext, vertexShaderPath, fragmentShaderPath)
        obj = pyobjloader.load_model(getPath(modelPath))

        position = np.array(position)

        verticesCombinedData = []
        indices = []

        numUniqueVertexData = 0
        uniqueVerticesData = {}
        for i in range(len(obj.point_indices)):
            vertexIndices = obj.point_indices[i]
            uvIndices = obj.uv_indices[i]
            for u in range(3):
                vertexIndex = vertexIndices[u]
                uvIndex = uvIndices[u]
                key = (vertexIndex, uvIndex)
                
                if key in uniqueVerticesData:
                    indices.append(uniqueVerticesData[key])
            
                else:
                    verticesCombinedData.extend((*(obj.vertex_points[vertexIndex] + position), *obj.vertex_uv[uvIndex]))
                    numUniqueVertexData += 1
                    uniqueVerticesData[key] = numUniqueVertexData - 1
                    indices.append(numUniqueVertexData - 1)

        verticesCombinedData = np.array(verticesCombinedData, dtype='f4')
        indices = np.array(indices, dtype='i4')

        self.vbo = glContext.buffer(verticesCombinedData.tobytes())
        self.ebo = glContext.buffer(indices.tobytes())
        self.vao = glContext.vertex_array(self.shaderProgram, [
            (self.vbo, '3f 2f', 'in_vertex', 'in_texcoord')
        ], self.ebo)

    def draw(self):
        self.vao.render()