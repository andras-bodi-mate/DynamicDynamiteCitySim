import pygame as pg

from window import Window
from camera import Camera
from scene import Scene

class App:
    def __init__(self):
        self.isRunning = True

        self.window = Window()
        self.camera = Camera(self.window, 80)
        self.scene = Scene(self.window)

        pg.mouse.set_visible(0)
        pg.event.set_grab(True)

    def close(self):
        self.isRunning = False

    def gameTick(self):
        self.scene.gameTick(self.deltaTime)

    def mainLoop(self):
        self.deltaTimeClock = pg.time.Clock()
        while self.isRunning:
            self.deltaTime = self.deltaTimeClock.tick() / 1000.0
            self.handleEvents()
            self.gameTick()
            self.draw()
        pg.quit()
        quit()

    def handleMouseDownEvents(self, button, pos):
        pass

    def handleMouseUpEvents(self, button, pos):
        pass

    def handleMouseMotionEvents(self, buttons, pos, relPos):
        self.camera.processRotationInput(relPos)

    def handleKeyHoldEvents(self, keys, modifiers):
        self.camera.processMovementInput(keys, self.deltaTime)

    def handleKeyPressEvents(self, key, modifiers):
        match key:
            case pg.K_ESCAPE:
                self.close()
            
            case pg.K_p:
                self.scene.city.constructBuilding()

            case pg.K_o:
                self.scene.city.importer.openAndImportFiles()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()

            if event.type == pg.KEYDOWN:
                self.handleKeyPressEvents(event.key, event.mod)

            if event.type == pg.MOUSEMOTION:
                self.handleMouseMotionEvents(event.buttons, event.pos, event.rel)

            if event.type == pg.MOUSEBUTTONDOWN:
                self.handleMouseDownEvents(event.button, event.pos)

            if event.type == pg.MOUSEBUTTONUP:
                self.handleMouseUpEvents(event.button, event.pos)

        self.handleKeyHoldEvents(pg.key.get_pressed(), pg.key.get_mods())

    def draw(self):
        self.camera.calculateViewMatrix()
        self.camera.updateUniforms(self.scene.city.buildingRenderer.mesh.shaderProgram)
        self.camera.updateUniforms(self.scene.city.streetRenderer.mesh.shaderProgram)
        self.window.glContext.clear()
        self.window.glContext.enable(self.window.glContext.DEPTH_TEST)
        self.scene.draw()
        pg.display.flip()