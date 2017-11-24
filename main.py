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

#the list of temperatures for the missing year
origTempRange = []

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

def daysBeforeAndAfter():
    for i in range(-date_range, date_range+1):
        if(i == 0):
            continue
        origTempRange.append(dates_temps[missing_date + timedelta(days=i)])

def findAvg():
    #the years other than the missing one
    otherYears = []

    #The list of temperatures for the other years, same dates
    otherYearsTemps = []

    #The list of difference in temperatures between the missing year and all other years
    diffList = []

    for i in dates_temps:
        if(i.month == missing_date.month and i.day == missing_date.day and i.year != missing_date.year):
            otherYears.append(i)

    listOfDates = []
    for i in dates_temps:
        for j in otherYears:
            if(i == j):
                listOfDates.append(i)

    listOfDates.sort()

    for i in listOfDates:
        listOfTemps = []
        for j in range(-date_range, date_range+1):
            if(j == 0):
                continue
            listOfTemps.append(dates_temps[i + timedelta(days=j)])
        otherYearsTemps.append(listOfTemps)

    for i in otherYearsTemps:
        tempList = []
        for j in range(0,2*date_range):
            tempList.append(abs(origTempRange[j] - i[j]))
        diffList.append(tempList)

    avg = []
    for i in diffList:
        s = 0
        for j in range(0,2*date_range):
            s += i[j]
        avg.append(round(s/(2*date_range), 3))

    avg2 = avg

    mins = []
    for j in range(3):
        minA = 10000
        for i in avg2:
            if(i < minA):
                minA = i
        avg2 = [10000 if x==minA else x for x in avg2]
        mins.append(minA)

    #find the indices of the mins
    tempList = []
    for i in range(3):
        for j in avg:
            if(mins[i] == j):
                tempList.append(avg.index(j))

    newList = []
    for i in tempList:
        newList.append(listOfDates[i])

    finalAns = 0
    for i in dates_temps:
        for j in newList:
            if(i == j):
                finalAns += dates_temps[i]
    finalAns = finalAns/3

    print("")
    print "The estimated temperature for", missing_date, "is", finalAns, "degrees fahrenheit"
    print "The actual temperature for", missing_date, "is", dates_temps[missing_date], "degrees fahrenheit"

gatherInput()
parseData()
daysBeforeAndAfter()
findAvg()
