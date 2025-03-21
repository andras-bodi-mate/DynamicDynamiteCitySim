import pygame as pg

import csv
import tkinter as tk
import tkinter.filedialog as fd

from datetime import date

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
        "Dolgozó": Occupation.Worker,
        "Nyugdíjas": Occupation.Retired
    }

    serviceTypes = {
        "Egészségügy": ServiceType.HealthCare,
        "Közlekedés": ServiceType.Transportation
    }

    fileTypes = [("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    
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
            id = int(id)
            buildingType = Importer.buildingTypes[buildingType]
            constructionDate = date.fromisoformat(constructionDate)
            usableArea = float(usableArea)

            self.buildingData.append(BuildingData(id, name, buildingType, constructionDate, usableArea))

    def importResidents(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, dateOfBirth, occupation, residence = row
            id = int(id)
            dateOfBirth = date.fromisoformat(dateOfBirth)
            occupation = Importer.occupationTypes[occupation]
            residence = int(residence)

            self.buildingData.append(Resident(id, name, dateOfBirth, occupation, residence))

    def importServices(self, fileName):
        for row in self.extractRowsFromFile(fileName):
            id, name, serviceType, affectedBuildings = row
            id = int(id)
            serviceType = Importer.serviceTypes[serviceType]
            affectedBuildings = map(int, affectedBuildings.split(' '))

            self.serviceData.append(Service(id, name, serviceType, affectedBuildings))

    def openAndImportFiles(self):
        pg.display.toggle_fullscreen()

        root = tk.Tk()
        root.withdraw()

        fileNames = (fd.askopenfilename(filetypes = Importer.fileTypes, defaultextension = ".csv") for _ in range(3))
        buildingsFileName, residentsFileName, servicesFileName = fileNames

        pg.display.toggle_fullscreen()

        #self.importBuildings(buildingsFileName)
        #self.importResidents(residentsFileName)
        #self.importServices(servicesFileName)