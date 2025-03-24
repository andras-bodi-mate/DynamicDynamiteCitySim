import moderngl as gl
import numpy as np
from pyglm import glm

from pathHandler import getPath
from shader import loadShaders
from material import Material
from obj import Obj

class SubMesh:
    def __init__(self, vertexData, faceData, shaderProgram, baseColorPath):
        self.glContext = gl.get_context()
        self.shaderProgram = shaderProgram

        self.material = Material(baseColorPath)

        self.vbo = self.glContext.buffer(vertexData.tobytes())
        self.ebo = self.glContext.buffer(faceData.tobytes())
        self.vao = self.glContext.vertex_array(shaderProgram, [
            (self.vbo, '3f 2f', 'in_vertex', 'in_texcoord')
        ], self.ebo)

        self.instancesVao = None
    
    def render(self):
        self.vao.render()

    def use(self):
        self.material.use()

class Mesh:
    def __init__(self, modelPath, vertexShaderPath, fragmentShaderPath, textures):
        self.glContext = gl.get_context()
        self.shaderProgram = loadShaders(vertexShaderPath, fragmentShaderPath)
        # objScene = assimp.ImportFile(getPath(modelPath), (assimp.Process_Triangulate))

        obj = Obj(getPath(modelPath))

        self.numMaterials = obj.numMaterials
        self.subMeshes: list[SubMesh] = []
        for materialIndex in range(obj.numMaterials):
            
            subMesh = SubMesh(obj.vertexDataPerMaterial[materialIndex],
                              obj.facesPerMaterial[materialIndex],
                              self.shaderProgram,
                              textures[obj.materials[materialIndex]])
            
            self.subMeshes.append(subMesh)

        self.numInstances = 0

    def render(self):
        for subMesh in self.subMeshes:
            subMesh.use()
            subMesh.render()

    def renderInstances(self):        
        for subMesh in self.subMeshes:
            if subMesh.instancesVao == None:
                return
            subMesh.use()
            subMesh.instancesVao.render(instances = self.numInstances)

    def updateInstances(self, instancePositions, instanceRotations):
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

        for subMesh in self.subMeshes:
            subMesh.instancesVao = self.glContext.vertex_array(self.shaderProgram, [
                (subMesh.vbo, '3f 2f', 'in_vertex', 'in_texcoord'),
                (transformsVbo, "16f/i", "in_instanceTransform"),
                (translationsVbo, "3f/i", "in_instanceTranslation")
            ], index_buffer=subMesh.ebo)

        self.numInstances = len(instancePositions)