import os
from resident import Resident
import csv
from dataclasses import dataclass
from enum import Enum
from datetime import date


@dataclass
class Resident:
    id: int
    name: str
    dateOfBirth: date
    occupation: int
    """
    1:Nincs
    2:Tanuló
    3:Tanár
    4:Tűzoltó
    5:Rendőr
    6:Orvos
    7:Irodai dolgozó
    8:Egyéb
    """
    residence: int
def read_dir():
    posoccupations=["nincs","tanuló","tanár","tűzoltó","rendőr","orvos","irodai dolgozó"]
    source=input("Adja meg az lakosok.csv fájl elérési útját!")    
    with open(source, mode='r', newline='') as file:
        reader = csv.reader(file)  
        for row in reader:
            row[0]=int(float(row[0]))
            row[2]=int(float(row[2]))
            row[4]=int(float(row[4]))
            
            try:
                row[3]=(posoccupations.index(row[3].lower())+1)
            except:
                row[3]=8
            
            resident=Resident(row[0],row[1],row[2],row[3],row[4])
            print(resident)
            
            
read_dir()