import os
from building import Building
import csv

data=[]

def read_dir():
    source=input("Adja meg az épületek.csv fájl elérési útját!")    
    with open(source, mode='r', newline='') as file:
        reader = csv.reader(file)  
        for row in reader:        
            row[0]=int(float(row[0]))
            row[3]=int(float(row[3]))
            print(row)
            
            
read_dir()