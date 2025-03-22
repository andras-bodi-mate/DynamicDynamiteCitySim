import moderngl as gl
import numpy as np
from pyglm import glm

from pathHandler import getPath
from shader import loadShaders
from obj import Obj

class SubMesh:
    def __init__(self, vertexData, faceData, shaderProgram):
        self.glContext = gl.get_context()

        self.vbo = self.glContext.buffer(vertexData.tobytes())
        self.ebo = self.glContext.buffer(faceData.tobytes())
        self.vao = self.glContext.vertex_array(shaderProgram, [
            (self.vbo, '3f 2f', 'in_vertex', 'in_texcoord')
        ], self.ebo)
    
    def draw(self):
        self.vao.render()

class Mesh:
    def __init__(self, modelPath, vertexShaderPath, fragmentShaderPath):
        self.glContext = gl.get_context()
        self.shaderProgram = loadShaders(vertexShaderPath, fragmentShaderPath)
        # objScene = assimp.ImportFile(getPath(modelPath), (assimp.Process_Triangulate))

        obj = Obj(getPath(modelPath))

        self.numMaterials = obj.numMaterials
        self.subMeshes = [SubMesh(obj.vertexDataPerMaterial[materialIndex], obj.facesPerMaterial[materialIndex], self.shaderProgram) for materialIndex in range(obj.numMaterials)]

        self.vaos = []
        self.numInstances = 0

    def draw(self):
        for subMesh in self.subMeshes:
            subMesh.draw()

    def drawInstances(self):
        if self.vaos == None:
            return
        
        for vao in self.vaos:
            vao.render(instances = self.numInstances)

    def updateInstances(self, instancePositions, instanceRotations):
        print(len(instancePositions))

        instanceTransforms = []
        for rot in instanceRotations:
            transform = glm.mat4(1.0)

            transform = glm.rotate(transform, glm.radians(rot[2]), glm.vec3(0, 0, 1))
            transform = glm.rotate(transform, glm.radians(rot[0]), glm.vec3(1, 0, 0))
            transform = glm.rotate(transform, glm.radians(rot[1]), glm.vec3(0, 1, 0))

            instanceTransforms.append(transform)

        instanceTransforms = np.array(instanceTransforms, dtype = np.float32)
        instancePositions = np.array([(pos[0], pos[1], pos[2]) for pos in instancePositions], dtype = np.float32)

        transformsVbo = self.glContext.buffer(instanceTransforms.tobytes())
        translationsVbo = self.glContext.buffer(instancePositions.tobytes())

        self.vaos.clear()
        for subMesh in self.subMeshes:
            vao = self.glContext.vertex_array(self.shaderProgram, [
                (subMesh.vbo, '3f 2f', 'in_vertex', 'in_texcoord'),
                (transformsVbo, "16f/i", "in_instanceTransform"),
                (translationsVbo, "3f/i", "in_instanceTranslation")
            ], index_buffer=subMesh.ebo)

            self.vaos.append(vao)

        self.numInstances = len(instancePositions)