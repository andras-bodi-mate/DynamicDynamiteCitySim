from os import path
projectDir = path.abspath(path.join(path.dirname(__file__), ".."))

def getPath(relativeProjectPath):
    return projectDir + "\\" + relativeProjectPath

def getRotationFromVector(vec):
    if vec.y == 0:
        if vec.x > 0:
            return 270.0
        else:
            return 90.0
    else:
        if vec.y > 0:
            return 0.0
        else:
            return 180.0