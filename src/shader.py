import moderngl as gl
import PyQt6.QtCore as qtc

from utilities import getPath

class OnShaderLoadedEvent(qtc.QObject):
    triggered = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()

    def emit(self):
        self.triggered.emit()

    def connect(self, slot):
        self.triggered.connect(slot)

onShaderLoad = OnShaderLoadedEvent()

def loadShaders(vertexShader, fragmentShader):
    glContext = gl.get_context()
    
    with open(getPath(vertexShader)) as vertexShaderFile:
        with open(getPath(fragmentShader)) as fragmentShaderFile:
            program = glContext.program(vertexShaderFile.read(), fragmentShaderFile.read())
            onShaderLoad.emit()
            return program