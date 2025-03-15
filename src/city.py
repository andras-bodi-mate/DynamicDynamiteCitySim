from building import Building, BuildingType, date

class City:
    def __init__(self, glContext):
        self.glContext = glContext
        self.buildings: list[Building] = []
        self.roads = []
    
    def constructBuilding(self):
        self.buildings.append(Building(self.glContext, 0, "building", BuildingType.Residential, date.today(), 750))

    def draw(self):
        for building in self.buildings:
            building.draw()
        
        for road in self.roads:
            road.draw()