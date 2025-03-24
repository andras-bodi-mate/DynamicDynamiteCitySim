import PyQt6.QtCore as qtc
import glm

from window import Window
from camera import Camera
from scene import Scene

class App:
    def __init__(self):
        self.isRunning = True

        self.deltaTimeClock = qtc.QElapsedTimer()

        self.window = Window()
        self.camera = Camera(self.window, 80)
        self.scene = Scene(self.window)

        self.window.mainWindow.constructBuildingButton.clicked.connect(
            lambda: self.scene.city.constructBuilding()
        )
        self.window.mainWindow.loadDatabaseButton.clicked.connect(
            lambda: self.scene.city.importFilesAndConstruct()
        )
        self.window.mainWindow.nextMonthButton.clicked.connect(
            lambda: self.updateToNextMonth()
        )
        self.window.mainWindow.viewport.eventHandler.mouseMoved.connect(
            self.handleMouseMotionEvents
        )

    def close(self):
        self.isRunning = False

    def gameTick(self):
        #self.scene.city.constructBuilding()
        self.scene.gameTick(self.deltaTime)
    
    def processEvents(self):
        self.window.processEvents()
        self.handleKeyHoldEvents()

        if not self.window.isOpen:
            self.isRunning = False

    def mainLoop(self):
        self.deltaTimeClock.start()

        while self.isRunning:
            self.deltaTime = self.deltaTimeClock.elapsed() / 1000.0
            self.deltaTimeClock.restart()

            self.processEvents()
            self.gameTick()
            self.render()
        
        self.window.close()

    def handleMouseDownEvents(self, button, pos):
        pass

    def handleMouseUpEvents(self, button, pos):
        pass

    def handleMouseMotionEvents(self, deltaPosX, deltaPosY):
        self.camera.processRotationInput(glm.ivec2(deltaPosX, deltaPosY))

    def handleKeyHoldEvents(self):
        self.camera.processMovementInput(self.deltaTime)

    def updateToNextMonth(self):
        self.scene.city.updateToNextMonth()

    def render(self):
        self.window.mainWindow.updateDateLabel(str(self.scene.city.date))
        self.camera.calculateViewMatrix()
        self.camera.updateUniforms(self.scene.city.buildingRenderer.mesh.shaderProgram)
        self.camera.updateUniforms(self.scene.city.streetRenderer.mesh.shaderProgram)
        self.camera.updateUniforms(self.scene.backdrop.shaderProgram)
        self.camera.updateUniforms(self.scene.horizon.shaderProgram, writeProjection = False)
        self.scene.horizon.updateUniforms(self.window.size, self.camera.fov)

        self.window.glContext.enable(self.window.glContext.DEPTH_TEST)
        self.window.glContext.clear(0.5, 0.7, 0.8)
        self.scene.render()
        self.window.mainWindow.viewport.swapBuffers()