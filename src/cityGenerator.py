import numpy as np
import pyglm.glm as glm

from intersection import IntersectionType

from dataclasses import dataclass
from random import seed, randint
from enum import Enum
from time import sleep

class Lot:
    def __init__(self, bottomLeft: glm.ivec2, topRight: glm.ivec2, level = 0, minDistance = 5, maxDistance = 7):
        self.bottomLeft = bottomLeft
        self.topRight = topRight
        self.width = topRight.x - bottomLeft.x
        self.height = topRight.y - bottomLeft.y

        self.level = level
        self.minDistance = minDistance
        self.maxDistance = maxDistance

        self.subLots = []

    def generate(self, streets):
        s = 3 ** self.level
        self.columns = []
        self.rows = []

        shape = randint(1, 3) if self.level == 0 else 3

        if shape & 1:
            x = self.bottomLeft.x + self.minDistance
            while x <= self.topRight.x - self.minDistance:
                self.columns.append(x)
                streets.append(Street(glm.ivec2(x, self.bottomLeft.y), glm.ivec2(x, self.topRight.y)))

                x += randint(self.minDistance * s, self.maxDistance * s)
        
        if shape & 2:
            y = self.bottomLeft.y + self.minDistance
            while y <= self.topRight.y - self.minDistance:
                self.rows.append(y)
                streets.append(Street(glm.ivec2(self.bottomLeft.x, y), glm.ivec2(self.topRight.x, y)))

                y += randint(self.minDistance * s, self.maxDistance * s)

        if self.level == 0:
            return

        self.columns.insert(0, self.bottomLeft.x)
        self.columns.append(self.topRight.x)
        self.rows.insert(0, self.bottomLeft.y)
        self.rows.append(self.topRight.y)
        
        for yi in range(len(self.rows)-1):
            for xi in range(len(self.columns)-1):
                newLot = Lot(glm.ivec2(self.columns[xi], self.rows[yi]),
                                        glm.ivec2(self.columns[xi + 1], self.rows[yi + 1]),
                                        self.level - 1,
                                        self.minDistance,
                                        self.maxDistance)
                newLot.generate(streets)
                self.subLots.append(newLot)

class Street:
    def __init__(self, startPos: glm.ivec2, endPos: glm.ivec2):
        self.startPos = startPos
        self.endPos = endPos
        self.length = abs(self.startPos.y - self.endPos.y) if self.startPos.x == self.endPos.x else abs(self.startPos.x - self.endPos.x)
        self.direction = (self.endPos - self.startPos) // self.length

@dataclass
class StreetSegment:
    pos: glm.ivec2
    isHorizontal: bool

@dataclass
class Building:
    pos: glm.ivec2
    direction: glm.ivec2

@dataclass
class Intersection:
    pos: glm.ivec2
    type: IntersectionType
    direction: glm.ivec2 = glm.ivec2(0, 0)


class CellType(Enum):
    Empty = 0
    Street = 1
    Intersection = 2
    Building = 3

class CityGenerator:
    def __init__(self, streetMinDistance = 5, streetMaxDistance = 7):
        self.numBuildings = 0
        self.streetMinDistance = streetMinDistance
        self.streetMaxDistance = streetMaxDistance

        self.mainLot = Lot(glm.ivec2(-25, -25), glm.ivec2(25, 25), 1, self.streetMinDistance, self.streetMaxDistance)
        self.buildings: list[Building] = []
        self.streets: list[Street] = []
        self.streetSegments: list[StreetSegment] = []
        self.intersections: list[Intersection] = []

        self.prevMaxDist = 0.0

    def generateStreets(self):
        self.mainLot.generate(self.streets)

    def distanceSquared(self, position: glm.ivec2):
        return position.x**2 + position.y**2
    
    def generateBuildings(self):
        cells = {}
        streetDirections = {}
        for street in self.streets:
            for t in range(0, street.length + 1):
                p = street.startPos + street.direction * t
                if p not in cells:
                    cells[p] = CellType.Street
                    streetDirections[p] = street.direction
                else:
                    if cells[p] == CellType.Street:
                        cells[p] = CellType.Intersection
        
            for pos, type in cells.items():
                if type == CellType.Street:
                    self.streetSegments.append(StreetSegment(pos, streetDirections[pos].y == 0))

                elif type == CellType.Intersection:
                    a = glm.ivec2(pos.x, pos.y + 1)
                    b = glm.ivec2(pos.x - 1, pos.y)
                    c = glm.ivec2(pos.x, pos.y - 1)
                    d = glm.ivec2(pos.x + 1, pos.y)

                    e = [p in cells and (cells[p] == CellType.Street or cells[p] == CellType.Intersection) for p in (a, b, c, d)]
                    n = sum(e)

                    direction = glm.ivec2(0, 0)
                    if n == 3:
                        if e[0] == False:
                            direction = glm.ivec2(0, -1)
                        elif e[1] == False:
                            direction = glm.ivec2(1, 0)
                        elif e[2] == False:
                            direction = glm.ivec2(0, 1)
                        elif e[3] == False:
                            direction = glm.ivec2(-1, 0)

                    intersectionType = IntersectionType.Three if n == 3 else IntersectionType.Four

                    self.intersections.append(Intersection(pos, intersectionType, direction))

        for street in self.streets:
            for t in range(0, street.length):
                if randint(1, 5) == 1:
                    shape = randint(1, 2)
                elif randint(1, 10) == 1:
                    shape = 0
                else:
                    shape = 3
                
                middle = street.startPos + street.direction * t
                perpendicular = glm.ivec2(-street.direction.y, street.direction.x)

                p1, p2 = middle + perpendicular, middle - perpendicular

                if shape & 1 and not (p1 in cells and cells[p1] != CellType.Empty):
                    self.buildings.append(Building(p1, -perpendicular))
                    cells[p1] = CellType.Building

                if shape & 2 and not (p2 in cells and cells[p2] != CellType.Empty):
                    self.buildings.append(Building(middle - perpendicular, perpendicular))
                    cells[p2] = CellType.Building

        self.buildings.sort(key = lambda building: self.distanceSquared(building.pos))
        self.streetSegments.sort(key = lambda street: self.distanceSquared(street.pos))
        self.intersections.sort(key = lambda intersection: self.distanceSquared(intersection.pos))

    def generate(self):
        self.generateStreets()
        self.generateBuildings()

    def constructNewBuilding(self):
        newBuilding = self.buildings[self.numBuildings]

        minDistance = self.prevMaxDist
        maxDistance = (self.distanceSquared(newBuilding.pos)**0.5 + 2)**2
        self.numBuildings += 1
        self.prevMaxDist = maxDistance

        newStreetSegments: list[StreetSegment] = []
        newIntersections: list[Intersection] = []

        for streetSegment in self.streetSegments:
            dist = self.distanceSquared(streetSegment.pos)
            if dist >= minDistance and dist < maxDistance:
                newStreetSegments.append(streetSegment)
        
        for intersection in self.intersections:
            dist = self.distanceSquared(intersection.pos)
            if dist >= minDistance and dist < maxDistance:
                newIntersections.append(intersection)

        return (newBuilding, newStreetSegments, newIntersections)

    def collectStreets(self, streets: list, lot):
        streets.extend(lot.streets)
        for subLot in lot.subLots:
            self.collectStreets(streets, subLot)
        return streets

    def getStreetPositions(self):
        return [streetSegments.pos for streetSegments in self.streetSegments if streetSegments.isVisible]
    
    def getStreetRotations(self):
        return [0 if streetSegments.isHorizontal else 90 for streetSegments in self.streetSegments if streetSegments.isVisible]

    def reset(self):
        self.prevMaxDist = 0.0
        self.numBuildings = 0

    def draw(self, buildings, streetSegments, intersections):
        minX = min([min(street.startPos.x, street.endPos.x) for street in self.streets])
        maxX = max([max(street.startPos.x, street.endPos.x) for street in self.streets])
        minY = min([min(street.startPos.y, street.endPos.y) for street in self.streets])
        maxY = max([max(street.startPos.y, street.endPos.y) for street in self.streets])

        size = glm.ivec2(maxX - minX + 3, maxY - minY + 3)
        origin = glm.ivec2(abs(minX) + 1, abs(minY) + 1)

        def setTile(p, v):
            self.tiles[p.y + origin.y, p.x + origin.x] = v

        self.tiles = np.full((size[1], size[0]), '·', dtype = str)

        for streetSegment in streetSegments:
            if streetSegment.isHorizontal:    
                setTile(streetSegment.pos, '═')
            else:
                setTile(streetSegment.pos, '‖')
        
        for building in buildings:
            setTile(building.pos, '■')

        for intersection in intersections:
            if intersection.type == IntersectionType.Four:
                setTile(intersection.pos, '╬')
                continue

            if intersection.direction.x == 0:
                if intersection.direction.y > 0:
                    setTile(intersection.pos, '╩')
                else:
                    setTile(intersection.pos, '╦')
            else:
                if intersection.direction.x > 0:
                    setTile(intersection.pos, '╠')
                else:
                    setTile(intersection.pos, '╣')

        for y in reversed(range(size[1])):
            print(' '.join(self.tiles[y]))

seed(1)