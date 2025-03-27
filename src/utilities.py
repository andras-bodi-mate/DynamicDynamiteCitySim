from os import path
from random import random
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
        
def normalisedRandom():
    return 2.0 * random() - 1.0