import numpy as np
import pygame as pg

from dataclasses import dataclass, field
from random import seed, random, randint
from math import floor, ceil

class Street:
    def __init__(self, startPos: tuple[int], endPos: tuple[int]):
        self.startPos = startPos
        self.endPos = endPos
        if startPos[1] == endPos[1]:
            self.direction = 0 if startPos[0] < endPos[0] else 2
        else:
            self.direction = 1 if startPos[1] < endPos[1] else 3
        self.length = abs(startPos[0] - endPos[0]) if self.direction == 0 else abs(startPos[1] - endPos[1])

        self.child1 = None
        self.child2 = None

    def fromParentStreet(parentStreet, startOffset, side, length):
        t = -1 if side == 0 else 1
        match parentStreet.direction:
            case 0:
                startPos = (parentStreet.startPos[0] + startOffset, parentStreet.startPos[1])
                endPos = (startPos[0], startPos[1] + length * t)
            case 1:
                startPos = (parentStreet.startPos[0], parentStreet.startPos[1] + startOffset)
                endPos = (startPos[0] + length * t, startPos[1])
            case 2:
                startPos = (parentStreet.startPos[0] - startOffset, parentStreet.startPos[1])
                endPos = (startPos[0], startPos[1] + length * t)
            case 3:
                startPos = (parentStreet.startPos[0], parentStreet.startPos[1] - startOffset)
                endPos = (startPos[0] + length * t, startPos[1])
        
        return Street(startPos, endPos)


class House:
    pos: tuple[float]

class CityGenerator:
    def __init__(self, streetMinDistance = 2):
        self.streetMinDistance = streetMinDistance

        self.houses: list[House] = []
        self.mainStreet = Street((1, 2), (8, 2))

    def generateStreet(self, parentStreet: Street):
        side = randint(0, 1)
        part = randint(0, 1)

        if parentStreet.length < 2 * self.streetMinDistance:
            return None
        startOffset = randint(self.streetMinDistance + 1, parentStreet.length - self.streetMinDistance - 1)
        length = parentStreet.length // 2

        newStreet = Street.fromParentStreet(parentStreet, startOffset, side, length)

        if part == 0:
            parentStreet.child1 = newStreet
        else:
            parentStreet.child2 = newStreet
        

    def generate(self):
        self.generateStreet(self.mainStreet)

    def collectStreets(self, streets: list[Street], currentStreet: Street):
        if currentStreet.child1 != None:
            streets.append(currentStreet.child1)
            self.collectStreets(streets, currentStreet.child1)

        elif currentStreet.child2 != None:
            streets.append(currentStreet.child2)
            self.collectStreets(streets, currentStreet.child2)

        return streets

    def drawTiles(self):
        self.tiles = np.zeros((10, 10), np.uint)
        streets = self.collectStreets([self.mainStreet], self.mainStreet)
        print(streets)
        for street in streets:
            for y in range(street.startPos[1], street.endPos[1]+1):
                for x in range(street.startPos[0], street.endPos[0]+1):
                    self.tiles[y, x] = 1

        print(self.tiles)

seed(0)
cityGenerator = CityGenerator()
cityGenerator.generate()
cityGenerator.drawTiles()