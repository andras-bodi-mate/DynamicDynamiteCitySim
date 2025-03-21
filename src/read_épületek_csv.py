from datetime import date
from enum import Enum
import os
import csv
from dataclasses import dataclass, field
@dataclass
class ReadBuilding:
    id: int
    name: str
    type: int
    """
    type:
    1: lakóház
    2: Oktatás(iskola)
    3: Tűzoltóság 
    4: Rendőrség
    5: Kórház
    6: Iroda
    7: Park
    8: Műv.ház
    9: Egyéb(nem felismert)
    """
    constructionDate: date
    usableArea: float
    
def read_dir():
    postypes=["Lakóház","Iskola", "Tűzoltóság","Rendőrség","Kórház","Iroda","Park","Művelődésiház"]
    buildings=[]
    source=input("Adja meg az épületek.csv fájl elérési útját!")    
    with open(source, mode='r', newline='') as file:
        reader = csv.reader(file)  
        for row in reader:        
            row[0]=int(float(row[0]))
            row[3]=int(float(row[3]))
            
            try:
                row[2]=(postypes.index(row[2])+1)
            except:
                row[2]=9
            
            
            building=ReadBuilding(row[0],row[1],row[2],row[3],row[4])
            buildings.append(building)
            
            
            
read_dir()