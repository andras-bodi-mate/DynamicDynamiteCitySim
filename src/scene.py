import glm
import pygame as pg
import numpy as np
import moderngl as gl
from pygame import Vector3 as Vec3

from city import City
from window import Window

class Scene:
    def __init__(self, window: Window):
        self.window = window
        self.city = City(window.glContext)

    def draw(self):
        self.city.draw()

    def gameTick(self, deltaTime):
        pass

