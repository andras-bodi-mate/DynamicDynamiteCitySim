import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
import moderngl as gl
import glm

from pathHandler import getPath

class ViewportEventHandler(qtc.QObject):
    mouseMoved = qtc.pyqtSignal(int, int)
    mousePressed = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.lastMousePos = None
    
    def getMouseDeltaPos(self, newPos):
        if not self.lastMousePos:
            self.lastMousePos = newPos
            return glm.ivec2(0, 0)
        
        deltaPos = newPos - self.lastMousePos
        self.lastMousePos = newPos
        return deltaPos

class Viewport(qtg.QWindow):
    def __init__(self):
        super().__init__()

        self.setSurfaceType(qtg.QWindow.SurfaceType.OpenGLSurface)
        self.setFlags(qtc.Qt.WindowType.FramelessWindowHint)
        self.setMouseGrabEnabled(True)

        self.eventHandler = ViewportEventHandler()

        fmt = qtg.QSurfaceFormat()
        fmt.setRenderableType(qtg.QSurfaceFormat.RenderableType.OpenGL)
        fmt.setProfile(qtg.QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        fmt.setVersion(3, 3)
        self.setFormat(fmt)

        self.glContext: gl.Context = None
        self.hasFocus = False

        self.context = qtg.QOpenGLContext(self)
        self.context.setFormat(self.format())
        self.context.create()
        self.context.makeCurrent(self)

    def getCenterPos(self):
        return self.position() + qtc.QPoint(self.width() // 2, self.height() // 2)

    def mouseMoveEvent(self, event):
        if self.hasFocus:
            center = self.getCenterPos()
            center = glm.ivec2(center.x(), center.y())
            newPos = event.position()
            newPos = glm.ivec2(newPos.x(), newPos.y())
            mouseDelta = newPos - center + glm.ivec2(9, 9) #TODO: Why is it off by 9 pixels on both axes?
            qtg.QCursor.setPos(center.x, center.y)
            self.eventHandler.mouseMoved.emit(mouseDelta.x, mouseDelta.y)

    def mousePressEvent(self, event):
        self.eventHandler.mousePressed.emit()

        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self.lockCursor()

    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key.Key_Escape:
            self.unlockCursor()

    def lockCursor(self):
        self.hasFocus = True
        self.setCursor(qtg.QCursor(qtc.Qt.CursorShape.BlankCursor))
        qtg.QGuiApplication.setOverrideCursor(qtc.Qt.CursorShape.BlankCursor)
        
        qtg.QCursor.setPos(self.getCenterPos())

    def unlockCursor(self):
        self.hasFocus = False
        self.setCursor(qtg.QCursor(qtc.Qt.CursorShape.ArrowCursor))
        qtg.QGuiApplication.restoreOverrideCursor()

    def swapBuffers(self):
        self.context.swapBuffers(self)

    def makeCurrent(self):
        self.context.makeCurrent(self)

class Button(qtw.QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedHeight(40)

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.isOpen = True
        self.setWindowTitle("Dynamic Dynamite - Városfejlesztési Szimuláció")
        self.setWindowIcon(qtg.QIcon(getPath("res\\images\\taskbarIcon.png")))

        mainContainer = qtw.QWidget()
        mainLayout = qtw.QVBoxLayout(mainContainer)

        self.constructBuildingButton = Button("Új épület építése")
        self.loadDatabaseButton = Button("Adatbázis betöltése")

        self.nextMonthButton = Button("Következő hónap")
        self.dateLabel = qtw.QLabel()
        self.dateLabel.setText("")
        self.dateLabel.setAlignment(qtc.Qt.AlignmentFlag.AlignHCenter)
        datePanelLayout = qtw.QVBoxLayout()
        datePanelLayout.setSpacing(5)
        datePanelLayout.addWidget(self.dateLabel)
        datePanelLayout.addWidget(self.nextMonthButton)

        datePanel = qtw.QWidget()
        datePanel.setLayout(datePanelLayout)

        bottomPanelLayout = qtw.QHBoxLayout()
        bottomPanelLayout.setSpacing(10)
        bottomPanelLayout.addWidget(self.constructBuildingButton)
        bottomPanelLayout.addWidget(self.loadDatabaseButton)
        bottomPanelLayout.addWidget(datePanel)
        bottomPanelLayout.addWidget(Button("Button4"))
        bottomPanelLayout.addWidget(Button("Button5"))

        bottomPanel = qtw.QWidget()
        bottomPanel.setLayout(bottomPanelLayout)
        bottomPanel.setFixedHeight(100)


        self.viewport = Viewport()
        viewportWidget = qtw.QWidget.createWindowContainer(self.viewport)
        mainLayout.addWidget(viewportWidget)
        mainLayout.addWidget(bottomPanel)

        self.setCentralWidget(mainContainer)

    def closeEvent(self, event):
        self.isOpen = False

    def updateDateLabel(self, text):
        self.dateLabel.setText(text)