import moderngl as gl
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import glm

from pathHandler import getPath
from ui import MainWindow

class Window:
    def __init__(self):
        self.qtApp = qtw.QApplication([])
        with open(getPath("res\\styles\\darkstyle.qss"), "r") as file:
            self.qtApp.setStyleSheet(file.read())

        self.mainWindow = MainWindow()
        self.mainWindow.showFullScreen()

        self.qtApp.processEvents()
        self.mainWindow.viewport.makeCurrent()
        self.glContext = gl.create_context()
        self.isOpen = True

        self.glContext.viewport = (0, 0, 1920, 1080)

        self.mainWindow.viewport.glContext = self.glContext

        primaryScreen = self.qtApp.primaryScreen()
        screenSize = primaryScreen.size()
        pixelRatio = primaryScreen.devicePixelRatio()
        self.size = glm.ivec2(screenSize.width() * pixelRatio, screenSize.height() * pixelRatio)
    
    def close(self):
        self.mainWindow.close()

    def processEvents(self):
        self.qtApp.processEvents()
        self.isOpen = self.mainWindow.isOpen