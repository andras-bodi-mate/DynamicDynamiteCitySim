import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
import moderngl as gl
import glm

from utilities import getPath
from city import City

class Viewport(qtg.QWindow):
    def __init__(self, qtApp):
        super().__init__()

        self.setSurfaceType(qtg.QWindow.SurfaceType.OpenGLSurface)
        self.setFlags(qtc.Qt.WindowType.FramelessWindowHint)
        self.setMouseGrabEnabled(True)

        fmt = qtg.QSurfaceFormat()
        fmt.setRenderableType(qtg.QSurfaceFormat.RenderableType.OpenGL)
        fmt.setProfile(qtg.QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        fmt.setVersion(3, 3)
        self.setFormat(fmt)

        self.glContext: gl.Context = None
        self.hasFocus = False

        primaryScreen = qtApp.primaryScreen()
        screenSize = primaryScreen.size()
        self.pixelRatio = primaryScreen.devicePixelRatio()
        self.center = glm.ivec2(screenSize.width() * self.pixelRatio / 2, screenSize.height() * self.pixelRatio / 2)

        self.context = qtg.QOpenGLContext(self)
        self.context.setFormat(self.format())
        self.context.create()
        self.context.makeCurrent(self)

    def centerCursor(self):
        qtg.QCursor.setPos(qtc.QPoint(int(self.center.x / self.pixelRatio), int(self.center.y / self.pixelRatio)))

    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.MouseButton.LeftButton:
            self.lockCursor()

    def keyPressEvent(self, event):
        if event.key() == qtc.Qt.Key.Key_Escape:
            self.unlockCursor()

    def lockCursor(self):
        if self.hasFocus == False:
            self.hasFocus = True
            self.setCursor(qtg.QCursor(qtc.Qt.CursorShape.BlankCursor))
            qtg.QGuiApplication.setOverrideCursor(qtc.Qt.CursorShape.BlankCursor)
            self.centerCursor()

    def unlockCursor(self):
        if self.hasFocus == True:
            self.hasFocus = False
            self.setCursor(qtg.QCursor(qtc.Qt.CursorShape.ArrowCursor))
            qtg.QGuiApplication.restoreOverrideCursor()
            self.centerCursor()

    def focusOutEvent(self, event):
        self.unlockCursor()

    def swapBuffers(self):
        self.context.swapBuffers(self)

    def makeCurrent(self):
        self.context.makeCurrent(self)

class Button(qtw.QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedHeight(40)

class StatisticsPopup(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.closeButton = Button("Close")
        layout = qtw.QVBoxLayout()
        self.averageResidentHappinessLabel = qtw.QLabel()
        self.averageBuildingConditionLabel = qtw.QLabel()
        layout.addWidget(self.averageResidentHappinessLabel)
        layout.addWidget(self.averageBuildingConditionLabel)
        layout.addWidget(self.closeButton)
        self.setLayout(layout)
        self.setFixedHeight(200)
        self.setWindowFlag(qtc.Qt.WindowType.FramelessWindowHint)

class MainWindow(qtw.QMainWindow):
    def __init__(self, qtApp):
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
        self.statisticsPopupButton = Button("Statisztika")

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
        bottomPanelLayout.addWidget(self.statisticsPopupButton)
        bottomPanelLayout.addWidget(Button("Button5"))

        bottomPanel = qtw.QWidget()
        bottomPanel.setLayout(bottomPanelLayout)
        bottomPanel.setFixedHeight(100)

        self.viewport = Viewport(qtApp)
        viewportWidget = qtw.QWidget.createWindowContainer(self.viewport)
        mainLayout.addWidget(viewportWidget)
        mainLayout.addWidget(bottomPanel)

        self.statisticsPopup = StatisticsPopup()

        self.setCentralWidget(mainContainer)

    def closeEvent(self, event):
        self.isOpen = False

    def updateDateLabel(self, text):
        self.dateLabel.setText(text)

class UI:
    def __init__(self):
        self.qtApp = qtw.QApplication([])
        with open(getPath("res\\styles\\darkstyle.qss"), "r") as file:
            self.qtApp.setStyleSheet(file.read())

        self.mainWindow = MainWindow(self.qtApp)
        self.mainWindow.showFullScreen()

        self.qtApp.processEvents()
        self.mainWindow.viewport.makeCurrent()
        self.glContext = gl.create_context()
        self.isOpen = True

        self.glContext.viewport = (0, 0, 1920, 1080)
        self.mainWindow.viewport.glContext = self.glContext

    def close(self):
        self.mainWindow.close()

    def processEvents(self):
        self.qtApp.processEvents()
        self.isOpen = self.mainWindow.isOpen

    def openStatisticsPopup(self, city: City):
        averageResidentHappiness, averageBuildingCondition = city.calculateStatistics()

        averageResidentHappinessText = f"Lakosok átlag boldogsága: {
            "%.2f" % averageResidentHappiness if averageResidentHappiness != None else "Nincsenek lakosok"
        }"
        averageBuildingConditionText = f"Épületeg átlag állapota: {
            "%.2f" % averageBuildingCondition if averageBuildingCondition != None else "Nincsenek épületek"
        }"

        self.mainWindow.statisticsPopup.averageResidentHappinessLabel.setText(averageResidentHappinessText)
        self.mainWindow.statisticsPopup.averageBuildingConditionLabel.setText(averageBuildingConditionText)

        self.mainWindow.statisticsPopup.exec()