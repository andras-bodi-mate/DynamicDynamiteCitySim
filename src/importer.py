import csv
import tkinter as tk
import tkinter.filedialog as fd

from utilities import getPath
from building import BuildingType, BuildingData
from resident import Resident, Occupation
from service import Service, ServiceType
from project import Project, ProjectType

from datetime import date

class Importer:
    buildingTypes = {
        "Lakóház": BuildingType.Residential,
        "Oktatás": BuildingType.Education,
        "Tűzoltóság": BuildingType.FireDepartment,
        "Rendőrség": BuildingType.Police,
        "Egészségügy": BuildingType.HealthCare,
        "Iroda": BuildingType.Office,
        "Önkormányzat": BuildingType.Governmental,
        "Művelődési ház": BuildingType.CommunityCenter,
        "Kereskedelem": BuildingType.Trade,
        "Sport": BuildingType.Sport,
        "Közlekedés": BuildingType.Transportation
    }

    occupationTypes = {
        "Nincs": Occupation.No,
        "Tanuló": Occupation.Student,
        "Orvos": Occupation.Doctor,
        "Rendőr": Occupation.Officer,
        "Irodai Dolgozó": Occupation.OfficeWorker,
        "Tanár": Occupation.Teacher,
        "Tűzoltó": Occupation.FireFighter,
        "Nyugdíjas": Occupation.Retired,
        "Polgármester": Occupation.Mayor
    }

    serviceTypes = {
        "Egészségügy": ServiceType.HealthCare,
        "Oktatás": ServiceType.Education,
        "Tűzoltóság": ServiceType.FireDepartment,
        "Közlekedés": ServiceType.Transportation
    }

    projectTypes = {
        "Lakosok Boldogságát Növelő": ProjectType.IncreasesResidentHappiness,
        "Épületek Állapotát Javító": ProjectType.ImprovesBuildingConditions,
        "Lakosok Boldogságát Növelő És Épületek Állapotát Javító": ProjectType.Both
    }

    fileTypes = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    fileDialogTitles = [f"Válassza ki a .csv fájlt ami tartalmazza a(z) {s} adatait." for s in (
        "épület típúsok", "foglalkozás típúsok", "szolgáltatás típúsok", "projekt típúsok",
        "épületek", "lakosok", "szolgáltatások", "városfejlesztési projektek"
    )]

    dateTimeFormat = r"%d/%m/%Y %H:%M:%S"

    def __init__(self):
        self.importedBuildingTypes = {}
        self.importedOccupationTypes = {}
        self.importedServiceTypes = {}
        self.importedProjectTypes = {}

        self.buildingData: list[BuildingData] = []
        self.residentData: list[Resident] = []
        self.serviceData: list[Service] = []
        self.projectData: list[Project] = []

    def getDateFromString(self, dateStr: str):
        dateStr = dateStr.replace(' ', '')
        year, month, day = map(int, dateStr.split('.')[:3])
        return date(year, month, day)

    def extractRowsFromFile(self, fileName):
        with open(fileName, mode = 'r', encoding = "utf-8") as file:
            for row in csv.reader(file):
                yield row

    def importBuildingTypes(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            value, typeName = row[:2]
            self.importedBuildingTypes[value] = typeName.strip()

    def importOccupationTypes(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            value, typeName = row[:2]
            self.importedOccupationTypes[value] = typeName.strip()

    def importServiceTypes(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            value, typeName = row[:2]
            self.importedServiceTypes[value] = typeName.strip()

    def importProjectTypes(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            value, typeName = row[:2]
            self.importedProjectTypes[value] = typeName.strip()

    def importBuildings(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, description, buildingType, constructionYear, usableArea = row[:5]
            id = int(id)
            buildingType = Importer.buildingTypes[self.importedBuildingTypes[buildingType.strip()]]
            constructionYear = int(constructionYear)
            usableArea = float(usableArea)

            self.buildingData.append(BuildingData(id, description, buildingType, constructionYear, usableArea,100))

    def importResidents(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, birthYear, occupation, residence = row[:5]
            id = int(id)
            birthYear = int(birthYear)
            occupation = Importer.occupationTypes[self.importedOccupationTypes[occupation.strip()]]
            residence = int(residence)

            self.residentData.append(Resident(id, name, birthYear, occupation, residence, 100))

    def importServices(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, serviceType, affectedBuildings = row[:4]
            id = int(id)
            serviceType = Importer.serviceTypes[self.importedServiceTypes[serviceType.strip()]]
            affectedBuildings = tuple(map(int, map(float, affectedBuildings.split(' '))))

            self.serviceData.append(Service(id, name, serviceType, affectedBuildings))

    def importProjects(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, description, projectType, cost, startDate, endDate = row[:6]
            id = int(id)
            projectType = Importer.projectTypes[self.importedProjectTypes[projectType.strip()]]
            cost = float(cost)
            startDate = self.getDateFromString(startDate)
            endDate = self.getDateFromString(endDate)

            self.projectData.append(Project(id, description, projectType, cost, startDate, endDate))

    def openAndImportFiles(self):
        root = tk.Tk()
        root.iconbitmap(getPath("res\\images\\dialogIcon.ico"))
        root.withdraw()

        fileNames = []
        for i in range(len(self.fileDialogTitles)):
            fileName = fd.askopenfilename(title = Importer.fileDialogTitles[i], filetypes = Importer.fileTypes, defaultextension = ".csv")
            if fileName != '':
                fileNames.append(fileName)
            else:
                return
        
        buildingTypesFileName, occupationTypesFileName, serviceTypesFileName, projectTypesFileName, buildingsFileName, residentsFileName, servicesFileName, projectsFileName = fileNames

        self.importBuildingTypes(buildingTypesFileName)
        self.importOccupationTypes(occupationTypesFileName)
        self.importServiceTypes(serviceTypesFileName)
        self.importProjectTypes(projectTypesFileName)

        self.importBuildings(buildingsFileName)
        self.importResidents(residentsFileName)
        self.importServices(servicesFileName)
        self.importProjects(projectsFileName)