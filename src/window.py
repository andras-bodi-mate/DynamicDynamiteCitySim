import moderngl as gl
import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc
import PyQt6.QtGui as qtg
import glm

from utilities import getPath
from ui import UI

class Window:
    def __init__(self):
        self.ui = UI()
        self.glContext = self.ui.glContext
        primaryScreen = self.ui.qtApp.primaryScreen()
        screenSize = primaryScreen.size()
        pixelRatio = primaryScreen.devicePixelRatio()
        self.size = glm.ivec2(screenSize.width() * pixelRatio, screenSize.height() * pixelRatio)
    
    def close(self):
        self.ui.close()

    def processEvents(self):
        self.ui.processEvents()
        self.isOpen = self.ui.isOpen