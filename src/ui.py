import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import PyQt6.QtCore as qtc
import moderngl as gl
import glm

from utilities import getPath
from city import City

from datetime import date
from project import Project
from service import Service

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
        self.numBuildingsLabel = qtw.QLabel()
        self.numResidentsLabel = qtw.QLabel()
        self.numServicesText = qtw.QLabel()
        self.numProjectsText = qtw.QLabel()

        layout.addWidget(self.averageResidentHappinessLabel)
        layout.addWidget(self.averageBuildingConditionLabel)
        layout.addWidget(self.numBuildingsLabel)
        layout.addWidget(self.numResidentsLabel)
        layout.addWidget(self.numServicesText)
        layout.addWidget(self.numProjectsText)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)
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

        self.minimumHappinessInput = qtw.QDoubleSpinBox(self)
        self.minimumHappinessInput.setMaximum(100_000_000_000)
        self.minimumHappinessInput.setValue(30.0)
        self.minimumHappinessInput.setGroupSeparatorShown(False)

        self.simulationStartDate = qtw.QDateEdit(self)
        self.simulationStartDate.setDate(qtc.QDate(today.year, today.month, today.day))

        self.simulationEndDate = qtw.QDateEdit(self)
        self.simulationEndDate.setDate(qtc.QDate(today.year + 5, today.month, today.day))

        startBudgetLabel = qtw.QLabel("Kezdő pénzkeretet (Ft):")
        minimumHappinessLabel = qtw.QLabel("Lakosok elvárt elégedettsége (%):")
        simulationStartLabel = qtw.QLabel("Szimulációs időszak kezdete:")
        simulationEndLabel = qtw.QLabel("Szimulációs időszak vége:")
        
        layout.setSpacing(15)
        layout.addWidget(startBudgetLabel, 0, 0)
        layout.addWidget(self.startingBudgetInput, 0, 1)

        layout.addWidget(minimumHappinessLabel, 1, 0)
        layout.addWidget(self.minimumHappinessInput, 1, 1)

        layout.addWidget(simulationStartLabel, 2, 0)
        layout.addWidget(self.simulationStartDate, 2, 1)

        layout.addWidget(simulationEndLabel, 3, 0)
        layout.addWidget(self.simulationEndDate, 3, 1)
        
        layout.addWidget(buttonBox, 4, 0, 1, 2, qtc.Qt.AlignmentFlag.AlignHCenter)
        
        buttonBox.accepted.connect(self.accept)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint)
    
    def getInputs(self):
        return (self.startingBudgetInput.value(),
                self.minimumHappinessInput.value(),
                self.simulationStartDate.date(),
                self.simulationEndDate.date())

class NewProjectInputDialog(qtw.QDialog):
    def __init__(self, projectTypes, ):
        super().__init__()
        buttonBox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok, self)
        layout = qtw.QGridLayout(self)

        today = date.today()

        descriptionLable = qtw.QLabel("Projekt leírás:")
        projectTypeLabel = qtw.QLabel("Projekt típusa:")
        costLabel = qtw.QLabel("Projekt költségei:")
        startDateLabel = qtw.QLabel("Projekt kezdési dátuma:")
        endDateLabel = qtw.QLabel("Projekt befejezési dátuma:")

        self.descriptionInput = qtw.QLineEdit(self)
        self.projectTypeInput = qtw.QComboBox(self)
        for projectType in projectTypes:
            self.projectTypeInput.addItem(projectType)
        self.projectTypeInput.setCurrentText(projectTypes[0])

        self.costInput = qtw.QDoubleSpinBox(self)
        self.costInput.setMaximum(100_000_000_000)
        self.costInput.setValue(500_000)
        self.costInput.setSingleStep(50_000)
        self.costInput.setGroupSeparatorShown(True)

        self.startDateInput = qtw.QDateEdit(self)
        self.startDateInput.setDate(qtc.QDate(today.year, today.month, today.day))

        self.endDateInput = qtw.QDateEdit(self)
        self.endDateInput.setDate(qtc.QDate(today.year + 1, today.month, today.day))

        layout.addWidget(descriptionLable, 0, 0)
        layout.addWidget(self.descriptionInput, 0, 1)

        layout.addWidget(projectTypeLabel, 1, 0)
        layout.addWidget(self.projectTypeInput, 1, 1)

        layout.addWidget(costLabel, 2, 0)
        layout.addWidget(self.costInput, 2, 1)

        layout.addWidget(startDateLabel, 3, 0)
        layout.addWidget(self.startDateInput, 3, 1)

        layout.addWidget(endDateLabel, 4, 0)
        layout.addWidget(self.endDateInput, 4, 1)

        layout.addWidget(buttonBox, 5, 0, 1, 2)

        buttonBox.accepted.connect(self.accept)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint)

    def getInputs(self):
        return (self.descriptionInput.text(),
                self.projectTypeInput.currentText(),
                self.costInput.value(),
                self.startDateInput.date(),
                self.endDateInput.date())

class NewServiceInputDialog(qtw.QDialog):
    def __init__(self, serviceTypes, ):
        super().__init__()
        buttonBox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok, self)
        layout = qtw.QGridLayout(self)

        today = date.today()

        descriptionLable = qtw.QLabel("Szolgáltatás leírás:")
        serviceTypeLabel = qtw.QLabel("Szolgáltatás típusa:")
        serviceAffectedBuildingLabel = qtw.QLabel("Szolgáltatás épülete:")

        self.descriptionInput = qtw.QLineEdit(self)
        self.serviceTypeInput = qtw.QComboBox(self)
        for serviceType in serviceTypes:
            self.serviceTypeInput.addItem(serviceType)
        self.serviceTypeInput.setCurrentText(serviceTypes[0])
        self.serviceAffectedBuildingInput = qtw.QLineEdit()
        self.serviceAffectedBuildingInput.setValidator(qtg.QIntValidator())

        layout.addWidget(descriptionLable, 0, 0)
        layout.addWidget(self.descriptionInput, 0, 1)

        layout.addWidget(serviceTypeLabel, 1, 0)
        layout.addWidget(self.serviceTypeInput, 1, 1)

        layout.addWidget(serviceAffectedBuildingLabel, 2, 0)
        layout.addWidget(self.serviceAffectedBuildingInput, 2, 1)

        layout.addWidget(buttonBox, 3, 0, 1, 2)

        buttonBox.accepted.connect(self.accept)
        self.setWindowFlags(qtc.Qt.WindowType.FramelessWindowHint)

    def getInputs(self):
        return (self.descriptionInput.text(),
                self.serviceTypeInput.currentText(),
                self.serviceAffectedBuildingInput.text())

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
        self.newProjectDialogButton = Button("Új projekt létrehozása")
        self.newServiceDialogButton = Button("Új szolgáltatás létrehozása")
        
        bottomPanelLayout = qtw.QVBoxLayout()
        bottomPanelButtonLayout = qtw.QHBoxLayout()
        bottomPanelButtonLayout.setSpacing(10)
        bottomPanelButtonLayout.addWidget(self.constructBuildingButton)
        bottomPanelButtonLayout.addWidget(self.loadDatabaseButton)
        bottomPanelButtonLayout.addWidget(self.nextMonthButton)
        bottomPanelButtonLayout.addWidget(self.statisticsPopupButton)
        bottomPanelButtonLayout.addWidget(self.newProjectDialogButton)
        bottomPanelButtonLayout.addWidget(self.newServiceDialogButton)

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
        date = city.currentDate
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
        numResidentsText = f"Lakosok száma: {
            len(city.residents)
        }"
        numBuildingsText = f"Épületek száma: {
            len(city.buildings)
        }"
        numServicesText = f"Szolgáltatások száma: {
            len(city.services)
        }"
        numProjectsText = f"Városfejlesztési projektek száma: {
            len(city.projects)
        }"

        self.mainWindow.statisticsPopup.averageResidentHappinessLabel.setText(averageResidentHappinessText)
        self.mainWindow.statisticsPopup.averageBuildingConditionLabel.setText(averageBuildingConditionText)
        self.mainWindow.statisticsPopup.numBuildingsLabel.setText(numBuildingsText)
        self.mainWindow.statisticsPopup.numResidentsLabel.setText(numResidentsText)
        self.mainWindow.statisticsPopup.numServicesText.setText(numServicesText)
        self.mainWindow.statisticsPopup.numProjectsText.setText(numProjectsText)

        self.mainWindow.statisticsPopup.exec()

    def openStartingConfigurationPopup(self, city: City):
        inputDialog = StartingConditionsInputDialog()
        if inputDialog.exec():
            startingBudget, minimumHappiness, startDate, endDate = inputDialog.getInputs()
            city.availableBudget = startingBudget
            city.minimumHappiness = minimumHappiness
            if endDate <= startDate:
                return
            city.currentDate = date(startDate.year(), startDate.month(), startDate.day())
            city.endDate = date(endDate.year(), endDate.month(), endDate.day())

    def addNewProject(self, city: City):
        inputDialog = NewProjectInputDialog(list(city.importer.projectTypes.keys()))
        if inputDialog.exec():
            description, projectType, cost, startDate, endDate = inputDialog.getInputs()
            newID = Project.getNewID(city.projects)
            projectType = city.importer.projectTypes[projectType]
            startDate = date(startDate.year(), startDate.month(), startDate.day())
            endDate = date(endDate.year(), endDate.month(), endDate.day())
            if endDate <= startDate:
                return
            city.projects.append(Project(newID, description, projectType, cost, startDate, endDate))

    def addNewService(self, city: City):
        inputDialog = NewServiceInputDialog(list(city.importer.serviceTypes.keys()))
        if inputDialog.exec():
            description, serviceType, affectedBuilding = inputDialog.getInputs()
            newID = Service.getNewID(city.services)
            serviceType = city.importer.serviceTypes[serviceType]
            try:
                affectedBuilding = int(float(affectedBuilding))
            except:
                return
            city.services.append(Service(newID, description, serviceType, [affectedBuilding]))