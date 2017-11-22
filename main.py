#----------------------------------------------------------------------------------------------
#   CPSC 4310 Project
#   Written By: Dawson Meyer and Eric Den Haan
#----------------------------------------------------------------------------------------------

import csv
from datetime import datetime, timedelta, date

#----------------------------------------------------------------------------------------------
# Global Variables
#----------------------------------------------------------------------------------------------

#The date for which we will estimate the temperature
missing_date = datetime.now()

#The number of days before and after to use in the estimation
date_range = 0

#The parsed dataset (dictionary of datetime/floats)
dates_temps = {}

#The location of the dataset
file_name = './dataset.csv'

#----------------------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------------------

#gatherInput Function
#Ask the user for global variables
#date_range is an int

def gatherInput():
    while True:
        print("Please enter a date between 1, 1, 1990 and 12, 31, 2004")
        print("Please enter the year for the missing date: ")
        try:
            year = int(raw_input())
        except ValueError:
            continue
        print("Please enter the month for the missing date: ")
        try:
            month = int(raw_input())
        except ValueError:
            continue
        print("Please enter the day for the missing date: ")
        try:
            day = int(raw_input())
        except ValueError:
            continue
        global missing_date
        missing_date = date(year, month, day)
        if not((missing_date >= date(1990, 1, 1))
            and (missing_date <= date(2004, 12, 31))):
            continue
        break

    while True:
        print("Please enter the number of days before and after to consider: ")
        try:
            global date_range
            date_range = int(raw_input())
        except ValueError:
            continue
        break

#parseData Function
#Read the .csv input file
#Populate a dictionary of date/avg temp
#date is a datetime object
#temp is a float

def parseData():
    with open(file_name, 'rb') as csvfile:
        global dates_temps
        for line in csvfile.readlines():
            array = line.split(',')
        num_cols = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile)
        next(reader)

        accept = ['-','0','1','2','3','4','5','6','7','8','9']

        for row in reader:
            date = row[2]
            date = date.replace("'", '')
            f_date = datetime.strptime(date, '%Y-%m-%d').date()

            temp = row[4]
            for char in temp:
                if(char not in accept):
                    temp = temp.replace(char, '')
            if(temp != ""):
                temp = float(temp)
                dates_temps[f_date] = temp
