import pygame as pg

class App:
    def __init__(self):
        displayInfo = pg.display.Info()
        self.windowSize = (displayInfo.current_w, displayInfo.current_h)
        self.surf = pg.display.set_mode(self.windowSize, pg.FULLSCREEN)
        self.isRunning = True

    def convX(self, tx):
        return self.windowSize[0] * tx
    
    def convY(self, ty):
        return self.windowSize[1] * ty

    def convXY(self, t2):
        return (self.convX(t2[0]), self.convY(t2[1]))
    
    def close(self):
        self.isRunning = False

    def gameTick(self):
        print(self.deltaTime)

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
        print(button, pos)

    def handleMouseUpEvents(self, button, pos):
        print(button, pos)

    def handleMouseMotionEvents(self, buttons, pos, relPos):
        print(buttons, pos, relPos)

    def handleKeyEvents(self, key, modifiers):
        match key:
            case pg.K_ESCAPE:
                self.close()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.close()
            if event.type == pg.KEYDOWN:
                self.handleKeyEvents(event.key, event.mod)
            if event.type == pg.MOUSEMOTION:
                self.handleMouseMotionEvents(event.buttons, event.pos, event.rel)
            if event.type == pg.MOUSEBUTTONDOWN:
                self.handleMouseDownEvents(event.button, event.pos)
            if event.type == pg.MOUSEBUTTONUP:
                self.handleMouseUpEvents(event.button, event.pos)

    def draw(self):
        self.surf.fill(0)
        pg.draw.circle(self.surf, (200, 100, 100), self.convXY((0.5, 0.5)), self.convX(0.05))
        pg.display.flip()