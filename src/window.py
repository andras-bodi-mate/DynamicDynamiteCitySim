import pygame as pg
import moderngl as gl
from pygame import Vector2 as Vec2
from pygame import Vector3 as Vec3

class Window:
    def __init__(self):
        displayInfo = pg.display.Info()
        self.size = Vec2(displayInfo.current_w, displayInfo.current_h)
        self.surf = pg.display.set_mode(self.size, pg.FULLSCREEN | pg.OPENGL | pg.DOUBLEBUF, vsync=1)
        self.glContext = gl.get_context()
    
    def close(self):
        pg.display.quit()

    def screenToWorld(self, p):
        o = (p - self.size/2)/100
        return Vec2(o.x, -o.y)
    
    def worldToScreen(self, p):
        return self.size/2 + 100*Vec2(p.x, -p.y)
    
    def worldXToScreen(self, x):
        return 100*x