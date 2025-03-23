import numpy as np

from pathHandler import getPath

class Obj:
    def __init__(self, fileName):
        vertices = []
        texCoords = []

        uniqueVerticesPerMaterial: list[dict[tuple, int]] = []
        self.facesPerMaterial: list[list[int]] = []

        currentMaterialIndex = -1
        self.materials = {}

        with open(fileName, 'r') as file:
            for line in file.readlines():
                lineParts = line.strip().split()
                if not lineParts:
                    continue
                
                # Vertex position
                if lineParts[0] == 'v':
                    vertices.append([float(x) for x in lineParts[1:4]])

                # Texture coordinates
                elif lineParts[0] == 'vt':
                    texCoords.append([float(x) for x in lineParts[1:3]])

                # Material change
                elif lineParts[0] == 'usemtl':
                    currentMaterialIndex += 1
                    self.materials[currentMaterialIndex] = lineParts[1]
                    self.facesPerMaterial.append([])
                    uniqueVerticesPerMaterial.append({})

                # Face (supports v/vt or v format)
                elif lineParts[0] == 'f':
                    for linePart in lineParts[1:]:
                        indices = linePart.split("/")
                        vertexIndex = int(indices[0]) - 1  # Convert to zero-based index
                        texCoordIndex = int(indices[1]) - 1
                        
                        key = (vertexIndex, texCoordIndex)
                        if not key in uniqueVerticesPerMaterial[currentMaterialIndex]:
                            i = len(uniqueVerticesPerMaterial[currentMaterialIndex])
                            uniqueVerticesPerMaterial[currentMaterialIndex][key] = i
                            self.facesPerMaterial[currentMaterialIndex].append(i)
                        else:
                            self.facesPerMaterial[currentMaterialIndex].append(uniqueVerticesPerMaterial[currentMaterialIndex][key])

        self.numMaterials = currentMaterialIndex + 1

        self.vertexDataPerMaterial = []
        for materialIndex in range(self.numMaterials):
            self.vertexDataPerMaterial.append([])
            for vertexIndex, texCoordIndex in uniqueVerticesPerMaterial[materialIndex].keys():
                self.vertexDataPerMaterial[-1].extend((*vertices[vertexIndex], *texCoords[texCoordIndex]))
            self.vertexDataPerMaterial[-1] = np.array(self.vertexDataPerMaterial[-1], dtype = "f4")
            self.facesPerMaterial[materialIndex] = np.array(self.facesPerMaterial[materialIndex], dtype = "i4")