import numpy as np
import pyglm.glm as glm

from dataclasses import dataclass, field
from random import seed, random, randint, choice
from math import floor, ceil
from enum import Enum

class Orientation(Enum):
    North = 0
    West = 1
    South = 2
    East = 3
    NorthWest = 4
    SouthWest = 5
    SouthEast = 6
    NorthEast = 7

class IntersectionType(Enum):
    Two = 0
    Three = 1
    Four = 2

@dataclass
class Intersection:
    position: glm.ivec2
    type: IntersectionType
    orientation: Orientation

class Street:
    def __init__(self, startPos: glm.ivec2, endPos: glm.ivec2):
        self.startPos = startPos
        self.endPos = endPos
        if startPos[1] == endPos[1]:
            self.orientation = Orientation.East if startPos[0] < endPos[0] else Orientation.West
        else:
            self.orientation = Orientation.South if startPos[1] < endPos[1] else Orientation.North

        if self.orientation == Orientation.East or self.orientation == Orientation.West:
            self.length = abs(startPos[0] - endPos[0])
        else:
            self.length = abs(startPos[1] - endPos[1])
        
        self.direction = (self.endPos - self.startPos) // self.length

    def fromParentStreet(parentStreet, middle, side, length):
        if side == 0:
            direction = glm.ivec2(-parentStreet.direction.y, parentStreet.direction.x)
        else:
            direction = glm.ivec2(parentStreet.direction.y, -parentStreet.direction.x)
        
        endPos = middle + direction * length

        return Street(middle + direction, endPos)
    
class House:
    pos: tuple[float]

class CityGenerator:
    def __init__(self, streetMinDistance = 2):
        self.streetMinDistance = streetMinDistance

        self.houses: list[House] = []
        self.streets: list[Street] = [Street(glm.ivec2(-7, 1), glm.ivec2(8, 1))]
        self.intersections: list[Intersection] = []

    def generateStreet(self, parentStreetIndex):
        parentStreet: Street = self.streets[parentStreetIndex]
        side = randint(0, 1)

        if parentStreet.length < 2 * self.streetMinDistance:
            return
        
        startOffset = randint(self.streetMinDistance, parentStreet.length - self.streetMinDistance)
        length = parentStreet.length // 2

        middlePos = parentStreet.startPos + parentStreet.direction * startOffset

        street1End = middlePos - parentStreet.direction
        street2Start = middlePos + parentStreet.direction

        self.streets.pop(parentStreetIndex)
        self.streets.append(Street(parentStreet.startPos, street1End))
        self.streets.append(Street(street2Start, parentStreet.endPos))
        self.streets.append(Street.fromParentStreet(parentStreet, middlePos, side, length))
        
        if parentStreet.direction.y == 0:
            intersectionOrientation = Orientation.North if (parentStreet.direction.x > 0) ^ side else Orientation.South
        else:
            intersectionOrientation = Orientation.West if (parentStreet.direction.y > 0) ^ side else Orientation.East

        self.intersections.append(Intersection(middlePos, IntersectionType.Three, intersectionOrientation))

    def generateStreets(self):
        for _ in range(8):
            available = [u for u in range(len(self.streets)) if self.streets[u].length >= (2 * self.streetMinDistance + 1)]
            if len(available) == 0:
                return
            streetIndex = choice(available)
            self.generateStreet(streetIndex)

    def generate(self):
        self.generateStreets()

    def drawTiles(self):
        minX = min([min(street.startPos.x, street.endPos.x) for street in self.streets])
        maxX = max([max(street.startPos.x, street.endPos.x) for street in self.streets])
        minY = min([min(street.startPos.y, street.endPos.y) for street in self.streets])
        maxY = max([max(street.startPos.y, street.endPos.y) for street in self.streets])

        size = glm.ivec2(maxX - minX + 10, maxY - minY + 10)

        def setTile(x, y, v):
            self.tiles[y + origin.y, x + origin.x] = v

        origin = glm.ivec2(abs(minX) + 1, abs(minY) + 1)
        self.tiles = np.full((size[0], size[1]), '·')

        print(len(self.streets))

        for street in self.streets:
            if street.orientation == Orientation.West or street.orientation == Orientation.East:
                if street.orientation == Orientation.East:
                    r = range(street.startPos.x, street.endPos.x + 1)
                else:
                    r = range(street.endPos.x, street.startPos.x + 1)

                for x in r:
                    setTile(x, street.startPos.y, '═')
            else:
                if street.orientation == Orientation.North:
                    r = range(street.endPos.y, street.startPos.y + 1)
                else:
                    r = range(street.startPos.y, street.endPos.y + 1)
                
                for y in r:
                    setTile(street.startPos.x, y, '‖')
        
        for intersection in self.intersections:
            match intersection.orientation:
                case Orientation.North:
                    setTile(intersection.position.x, intersection.position.y, '╩')
                    
                case Orientation.West:
                    setTile(intersection.position.x, intersection.position.y, '╣')

                case Orientation.South:
                    setTile(intersection.position.x, intersection.position.y, '╦')

                case Orientation.East:
                    setTile(intersection.position.x, intersection.position.y, '╠')

        for y in range(size[0]-1, -1, -1):
            print(' '.join(self.tiles[y]))

seed(0)
cityGenerator = CityGenerator()
cityGenerator.generate()
cityGenerator.drawTiles()