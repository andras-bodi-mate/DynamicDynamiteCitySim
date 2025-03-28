import PyQt6.QtCore as qtc
import glm

from inputHandler import InputHandler
from window import Window
from camera import Camera
from scene import Scene

class App:
    def __init__(self):
        self.isRunning = True
        self.didRender = False

        self.deltaTimeClock = qtc.QElapsedTimer()

        self.window = Window()
        self.camera = Camera(self.window, 80)
        self.scene = Scene()

        self.inputHandler = InputHandler(self.window.ui.mainWindow.viewport.center)

        self.window.ui.mainWindow.constructBuildingButton.clicked.connect(
            lambda: self.scene.city.constructBuilding()
        )
        self.window.ui.mainWindow.loadDatabaseButton.clicked.connect(
            lambda: self.scene.city.importFilesAndConstruct()
        )
        self.window.ui.mainWindow.nextMonthButton.clicked.connect(
            lambda: self.updateToNextMonth()
        )
        self.window.ui.mainWindow.statisticsPopupButton.clicked.connect(
            lambda: self.window.ui.openStatisticsPopup(self.scene.city)
        )
        self.window.ui.mainWindow.statisticsPopup.closeButton.clicked.connect(
            lambda: self.window.ui.mainWindow.statisticsPopup.close()
        )
        self.window.ui.mainWindow.newProjectDialogButton.clicked.connect(
            lambda: self.window.ui.addNewProject(self.scene.city)
        )
        self.window.ui.mainWindow.newServiceDialogButton.clicked.connect(
            lambda: self.window.ui.addNewService(self.scene.city)
        )

    def close(self):
        self.isRunning = False

    def gameTick(self):
        self.window.ui.mainWindow.updateLabels(self.scene.city)
        if not self.scene.city.hasBeenConfigured and self.didRender:
            self.window.ui.openStartingConfigurationPopup(self.scene.city)
            self.scene.city.hasBeenConfigured = True
        
        self.scene.gameTick(self.deltaTime)
    
    def processEvents(self):
        self.window.processEvents()
        self.handleKeyHoldEvents()
        self.handleMouseMotionEvents()

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

    def handleMouseMotionEvents(self):
        if self.window.ui.mainWindow.viewport.hasFocus:
            mouseDelta = self.inputHandler.getMouseDelta()
            if mouseDelta != None:
                self.camera.processRotationInput(mouseDelta)

    def handleKeyHoldEvents(self):
        self.camera.processMovementInput(self.inputHandler, self.deltaTime)

    def updateToNextMonth(self):
        if not self.scene.city.updateToNextMonth():
            self.close()

    def render(self):
        self.camera.calculateViewMatrix()
        self.camera.updateUniforms(self.scene.city.buildingRenderer.mesh.shaderProgram)
        self.camera.updateUniforms(self.scene.city.streetRenderer.mesh.shaderProgram)
        self.camera.updateUniforms(self.scene.backdrop.shaderProgram)
        self.camera.updateUniforms(self.scene.horizon.shaderProgram, writeProjection = False)
        self.scene.horizon.updateUniforms(self.window.size, self.camera.fov)

        self.window.glContext.enable(self.window.glContext.DEPTH_TEST)
        self.window.glContext.clear(0.0, 0.0, 0.0)
        self.scene.render()
        self.window.ui.mainWindow.viewport.swapBuffers()

        self.didRender = True