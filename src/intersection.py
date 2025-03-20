from enum import Enum

class IntersectionType(Enum):
    Three = 0
    Four = 1

class Intersection:
    def __init__(self, position, intersectionType, rotation):
        self.position = position
        self.intersectionType = intersectionType
        self.rotation = rotation