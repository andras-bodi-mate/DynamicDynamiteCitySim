import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
import moderngl as gl
import glm

from utilities import getPath
from city import City

from datetime import date

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

class StartingConditionsInputDialog(qtw.QDialog):
    def __init__(self):
        super().__init__()
        buttonBox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok, self)
        layout = qtw.QGridLayout(self)

        today = date.today()

        self.startingBudgetInput = qtw.QDoubleSpinBox(self)
        self.startingBudgetInput.setMaximum(100_000_000_000)
        self.startingBudgetInput.setValue(10_000_000)
        self.startingBudgetInput.setGroupSeparatorShown(True)
        self.startingBudgetInput.setSingleStep(100_000)

        self.simulationStartDate = qtw.QDateEdit(self)
        self.simulationStartDate.setDate(qtc.QDate(today.year, today.month, today.day))

        self.simulationEndDate = qtw.QDateEdit(self)
        self.simulationEndDate.setDate(qtc.QDate(today.year + 5, today.month, today.day))

        startBudgetLabel = qtw.QLabel("Kezdő pénzkeretet (Ft):")
        simulationStartLabel = qtw.QLabel("Szimulációs időszak kezdete:")
        simulationEndLabel = qtw.QLabel("Szimulációs időszak vége:")
        
        layout.setSpacing(15)
        layout.addWidget(startBudgetLabel, 0, 0)
        layout.addWidget(self.startingBudgetInput, 0, 1)

        layout.addWidget(simulationStartLabel, 1, 0)
        layout.addWidget(self.simulationStartDate, 1, 1)

        layout.addWidget(simulationEndLabel, 2, 0)
        layout.addWidget(self.simulationEndDate, 2, 1)
        
        layout.addWidget(buttonBox, 3, 0, 1, 2, qtc.Qt.AlignmentFlag.AlignHCenter)
        
        buttonBox.accepted.connect(self.accept)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint)
    
    def getInputs(self):
        return (self.startingBudgetInput.value(),
                self.simulationStartDate.date(),
                self.simulationEndDate.date())

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
        self.statisticsPopupButton = Button("Statisztika")
        
        bottomPanelLayout = qtw.QVBoxLayout()
        bottomPanelButtonLayout = qtw.QHBoxLayout()
        bottomPanelButtonLayout.setSpacing(10)
        bottomPanelButtonLayout.addWidget(self.constructBuildingButton)
        bottomPanelButtonLayout.addWidget(self.loadDatabaseButton)
        bottomPanelButtonLayout.addWidget(self.nextMonthButton)
        bottomPanelButtonLayout.addWidget(self.statisticsPopupButton)
        bottomPanelButtonLayout.addWidget(Button("Button5"))

        self.dateLabel = qtw.QLabel("")
        self.availableBudgetLabel = qtw.QLabel("")
        self.averageResidentHappinessLabel = qtw.QLabel("")

        self.dateLabel.setAlignment(qtc.Qt.AlignmentFlag.AlignHCenter)
        self.availableBudgetLabel.setAlignment(qtc.Qt.AlignmentFlag.AlignHCenter)
        self.averageResidentHappinessLabel.setAlignment(qtc.Qt.AlignmentFlag.AlignHCenter)

        bottomInformationPanelLayout = qtw.QHBoxLayout()
        bottomInformationPanelLayout.addWidget(self.availableBudgetLabel)
        bottomInformationPanelLayout.addWidget(self.dateLabel)
        bottomInformationPanelLayout.addWidget(self.averageResidentHappinessLabel)

        bottomInformationPanel = qtw.QWidget()
        bottomInformationPanel.setLayout(bottomInformationPanelLayout)
        bottomInformationPanel.setFixedHeight(50)

        botomButtonPanel = qtw.QWidget()
        botomButtonPanel.setLayout(bottomPanelButtonLayout)
        botomButtonPanel.setFixedHeight(50)

        bottomPanelLayout.setSpacing(0)
        bottomPanelLayout.addWidget(bottomInformationPanel)
        bottomPanelLayout.addWidget(botomButtonPanel)

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

    def updateLabels(self, city: City):
        date = city.date
        budget = city.availableBudget
        averageHappiness = sum([resident.happiness for resident in city.residents]) / len(city.residents) if len(city.residents) != 0 else None

        if date != None:
            self.dateLabel.setText(str(date))
        else:
            self.dateLabel.setText("Nincs megadva szimuláció időintervallum")

        if budget != None:
            self.availableBudgetLabel.setText(f"Pénzkeret: {budget:,.2f} Ft")
        else:
            self.availableBudgetLabel.setText("Nincs megadva pénzkeret")

        if averageHappiness != None:
            self.averageResidentHappinessLabel.setText(f"Lakosok átlag boldogsága: {averageHappiness:.2f} %")
        else:
            self.averageResidentHappinessLabel.setText("Nincsenek lakosok")

class UI:
    def __init__(self):
        self.qtApp = qtw.QApplication([])
        qtc.QDir.addSearchPath("icons", getPath("res\\styles\\icons\\"))
        with open(getPath("res\\styles\\dark\\darkstyle.qss"), "r") as file:
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
            "%.2f" % averageResidentHappiness + " %" if averageResidentHappiness != None else "Nincsenek lakosok"
        }"
        averageBuildingConditionText = f"Épületeg átlag állapota: {
            "%.2f" % averageBuildingCondition + " %" if averageBuildingCondition != None else "Nincsenek épületek"
        }"

        self.mainWindow.statisticsPopup.averageResidentHappinessLabel.setText(averageResidentHappinessText)
        self.mainWindow.statisticsPopup.averageBuildingConditionLabel.setText(averageBuildingConditionText)

        self.mainWindow.statisticsPopup.exec()

    def openStartingConfigurationPopup(self, city: City):
        inputDialog = StartingConditionsInputDialog()
        if inputDialog.exec():
            startingBudget, startDate, endDate = inputDialog.getInputs()
            city.availableBudget = startingBudget
            city.date = date(startDate.year(), startDate.month(), startDate.day())
            city.endDate = date(endDate.year(), endDate.month(), endDate.day())