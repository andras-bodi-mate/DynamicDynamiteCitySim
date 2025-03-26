import csv
import tkinter as tk
import tkinter.filedialog as fd

from datetime import datetime

from utilities import getPath
from building import BuildingType, BuildingData
from resident import Resident, Occupation
from service import Service, ServiceType

class Importer:
    buildingTypes = {
        "Lakóház": BuildingType.Residential,
        "Iskola": BuildingType.School,
        "Tűzoltóság": BuildingType.FireDepartment,
        "Rendőrség": BuildingType.Police,
        "Kórház": BuildingType.Hospital,
        "Iroda": BuildingType.Office,
        "Művelődési ház": BuildingType.CommunityCenter
    }

    occupationTypes = {
        "Nincs": Occupation.No,
        "Tanuló": Occupation.Student,
        "Orvos": Occupation.Doctor,
        "Rendőr": Occupation.Officer,
        "Irodai dolgozó": Occupation.OfficeWorker,
        "Tanár": Occupation.Teacher,
        "Tűzoltó": Occupation.FireFighter,
        "Nyugdíjas": Occupation.Retired
    }

    serviceTypes = {
        "Egészségügy": ServiceType.HealthCare,
        "Oktatás": ServiceType.Education,
        "Tűzoltóság": ServiceType.FireDepartment
    }

    fileTypes = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    fileDialogTitles = [f"Válassza ki a .csv fájlt ami tartalmazza a(z) {s} adatait." for s in ("épületek", "lakosok", "szolgáltatások")]

    dateTimeFormats = (r"%d/%m/%Y %H:%M:%S", r"%d/%m/%Y %H:%M:%S")

    def __init__(self):
        self.buildingData: list[BuildingData] = []
        self.residentData: list[Resident] = []
        self.serviceData: list[Service] = []

    def extractRowsFromFile(self, fileName):
        with open(fileName, mode='r') as file:
            for row in csv.reader(file):
                yield row

    def importBuildings(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, buildingType, constructionDate, usableArea = row
            id = int(float(id))
            buildingType = Importer.buildingTypes[buildingType]
            constructionDate = datetime.strptime(constructionDate, Importer.dateTimeFormat)
            usableArea = float(usableArea)

            self.buildingData.append(BuildingData(id, name, buildingType, constructionDate, usableArea,100))

    def importResidents(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, dateOfBirth, occupation, residence = row
            id = int(float(id))
            dateOfBirth = datetime.strptime(dateOfBirth, Importer.dateTimeFormat)
            occupation = Importer.occupationTypes[occupation]
            residence = int(float(residence))

            self.buildingData.append(Resident(id, name, dateOfBirth, occupation, residence, 100))

    def importServices(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, serviceType, affectedBuildings = row
            id = int(float(id))
            serviceType = Importer.serviceTypes[serviceType]
            affectedBuildings = map(int, map(float, affectedBuildings.split(' ')))

            self.serviceData.append(Service(id, name, serviceType, affectedBuildings))

    def openAndImportFiles(self):
        root = tk.Tk()
        root.iconbitmap(getPath("res\\images\\dialogIcon.ico"))
        root.withdraw()

        fileNames = []
        for i in range(3):
            fileName = fd.askopenfilename(title = Importer.fileDialogTitles[i], filetypes = Importer.fileTypes, defaultextension = ".csv")
            if fileName != '':
                fileNames.append(fileName)
            else:
                return
        
        buildingsFileName, residentsFileName, servicesFileName = fileNames

        self.importBuildings(buildingsFileName)
        self.importResidents(residentsFileName)
        self.importServices(servicesFileName)