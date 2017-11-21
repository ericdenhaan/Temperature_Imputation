#----------------------------------------------------------------------------------------------
#   CPSC 4310 Project
#   Written By: Dawson Meyer and Eric Den Haan
#----------------------------------------------------------------------------------------------

import csv
from datetime import datetime

#Note: Large gap in data from 1994-09-21 to 1996-07-01
#760 days missing in total

#----------------------------------------------------------------------------------------------
# Global Variables
#----------------------------------------------------------------------------------------------

dates_temps = {}
file_name = './dataset.csv'

#----------------------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------------------

#Read the .csv input file
#Return a dictionary of date/avg temp
#date is a datetime object
#temp is a float

def parseData():
    with open(file_name, 'rb') as csvfile:
        for line in csvfile.readlines():
            array = line.split(',')
        num_cols = len(array)
        csvfile.seek(0)
        
        reader = csv.reader(csvfile)
        next(reader)
        
        accept = ['-','0','1','2','3','4','5','6','7','8','9']
        
        for row in reader:
            date = row[5]
            date = date.replace("'", '')
            f_date = datetime.strptime(date, '%Y-%m-%d %H:%M')
            f_date = f_date.date()
            temp = row[28]
            for char in temp:
                if(char not in accept):
                    temp = temp.replace(char, '')
            if(temp != ""):
                temp = float(temp)
                dates_temps[f_date] = temp

parseData()