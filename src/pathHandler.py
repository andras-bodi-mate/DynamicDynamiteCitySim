from os import path
baseDir = path.abspath(path.join(path.dirname(__file__), ".."))

def getPath(projectPath):
    return baseDir + "\\" + projectPath