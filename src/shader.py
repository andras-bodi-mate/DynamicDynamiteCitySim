import moderngl as gl

from pathHandler import getPath

def loadShaders(vertexShader, fragmentShader):
    glContext = gl.get_context()
    
    with open(getPath(vertexShader)) as vertexShaderFile:
        with open(getPath(fragmentShader)) as fragmentShaderFile:
            return glContext.program(vertexShaderFile.read(), fragmentShaderFile.read())