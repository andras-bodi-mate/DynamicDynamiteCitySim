from os import path
projectDir = path.abspath(path.join(path.dirname(__file__), ".."))

def getPath(relativeProjectPath):
    return projectDir + "\\" + relativeProjectPath