import csv
import tkinter as tk
import tkinter.filedialog as fd

from utilities import getPath
from building import BuildingType, BuildingData
from resident import Resident, Occupation
from service import Service, ServiceType

class Importer:
    buildingTypes = {
        "Lakóház": BuildingType.Residential,
        "Oktatás": BuildingType.Education,
        "Tűzoltóság": BuildingType.FireDepartment,
        "Rendőrség": BuildingType.Police,
        "Egészségügy": BuildingType.HealthCare,
        "Iroda": BuildingType.Office,
        "Kormányzati": BuildingType.Governmental,
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
        "Irodai dolgozó": Occupation.OfficeWorker,
        "Tanár": Occupation.Teacher,
        "Tűzoltó": Occupation.FireFighter,
        "Nyugdíjas": Occupation.Retired
    }

    serviceTypes = {
        "Egészségügy": ServiceType.HealthCare,
        "Oktatás": ServiceType.Education,
        "Tűzoltóság": ServiceType.FireDepartment,
        "Közlekedés": ServiceType.Transportation
    }

    fileTypes = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    fileDialogTitles = [f"Válassza ki a .csv fájlt ami tartalmazza a(z) {s} adatait." for s in ("épületek", "lakosok", "szolgáltatások")]

    dateTimeFormat = r"%d/%m/%Y %H:%M:%S"

    def __init__(self):
        self.buildingData: list[BuildingData] = []
        self.residentData: list[Resident] = []
        self.serviceData: list[Service] = []

    def extractRowsFromFile(self, fileName):
        with open(fileName, mode = 'r') as file:
            for row in csv.reader(file):
                yield row

    def importBuildings(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, buildingType, constructionYear, usableArea = row
            id = int(float(id))
            buildingType = Importer.buildingTypes[buildingType.strip()]
            constructionYear = int(float(constructionYear))
            usableArea = float(usableArea)

            self.buildingData.append(BuildingData(id, name, buildingType, constructionYear, usableArea,100))

    def importResidents(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, birthYear, occupation, residence = row
            id = int(float(id))
            birthYear = int(float(birthYear))
            occupation = Importer.occupationTypes[occupation.strip()]
            residence = int(float(residence))

            self.residentData.append(Resident(id, name, birthYear, occupation, residence, 100))

    def importServices(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, serviceType, affectedBuildings = row
            id = int(float(id))
            serviceType = Importer.serviceTypes[serviceType.strip()]
            affectedBuildings = tuple(map(int, map(float, affectedBuildings.split(' '))))

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