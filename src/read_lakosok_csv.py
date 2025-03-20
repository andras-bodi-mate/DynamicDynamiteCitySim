import os
from resident import Resident
import csv

def read_dir():
    source=input("Adja meg az lakosok.csv fájl elérési útját!")    
    with open(source, mode='r', newline='') as file:
        reader = csv.reader(file)  
        for row in reader:
            row[0]=int(float(row[0]))
            row[2]=int(float(row[2]))
            row[4]=int(float(row[4]))
            if(row[3].lower()=="nincs"):
                row[3]=0
            elif(row[3].lower()=="diák"):
                row[3]=1
            elif(row[3].lower()=="nyugdíjas"):
                row[3]=3
            else:
                row[3]=2
            
            resident=Resident(row[0],row[1],row[2],row[3],row[4])
            print(resident)
            
            
read_dir()