from pathHandler import getPath

def loadShaders(glContext, vertexShader, fragmentShader):
    with open(getPath(vertexShader)) as vertexShaderFile:
        with open(getPath(fragmentShader)) as fragmentShaderFile:
            return glContext.program(vertexShaderFile.read(), fragmentShaderFile.read())