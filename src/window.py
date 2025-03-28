import moderngl as gl
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import glm

from utilities import getPath
from loadingScreen import LoadingScreen
from shader import onShaderLoad
from ui import UI

from time import sleep

class Window:
    def __init__(self):
        self.ui = UI()
        self.glContext = self.ui.glContext
        primaryScreen = self.ui.qtApp.primaryScreen()
        screenSize = primaryScreen.size()
        pixelRatio = primaryScreen.devicePixelRatio()
        self.size = glm.ivec2(screenSize.width() * pixelRatio, screenSize.height() * pixelRatio)

        self.loadingScreen = LoadingScreen(4, self.ui.mainWindow.viewport)
        onShaderLoad.connect(self.loadingScreen.increment)
    
    def close(self):
        self.ui.close()

    def processEvents(self):
        self.ui.processEvents()
        self.isOpen = self.ui.isOpen