#----------------------------------------------------------------------------------------------
#   CPSC 4310 Project
#   full_analysis.py
#   Written By: Dawson Meyer and Eric Den Haan
#----------------------------------------------------------------------------------------------

import csv
from datetime import datetime, timedelta, date

#----------------------------------------------------------------------------------------------
# Global Variables
#----------------------------------------------------------------------------------------------

#The number of days before and after to use in the estimation
date_range = 0

#The parsed dataset (dictionary of datetime/floats)
dates_temps = {}

#The location of the dataset
infile_name = './dataset.csv'

#The location of the dataset
outfile_name = './log_' + str(datetime.now()) +'.txt'

#----------------------------------------------------------------------------------------------
# Functions
#----------------------------------------------------------------------------------------------

#runAnalysis Function
#Ask the user for the number of days before and after to consider
#Run the temperature imputation for every date in the dataset
#Populate a log file with date, estimated temp, actual temp, difference
#Provide an overall accuracy measure
def runAnalysis():
    while True:
        print("Please enter the number of days before and after to consider: ")
        try:
            global date_range
            date_range = int(raw_input())
        except ValueError:
            continue
        break

    with open(outfile_name, 'w+') as logfile:
        logfile.write("Date    -    Actual    -    Estimate    -    Difference\n")
        estimates = []
        for i in sorted(dates_temps):
            if(i >= date(1990, 1, 1) and i <= date(2004, 12, 31)):
                est = findAvg(i)
                diff = abs(est - dates_temps[i])
                line = str(i) + "   -   " + str(dates_temps[i])
                line += "    -    " + str(est) + "    -    " + str(diff) + "\n"
                logfile.write(line)
                estimates.append(diff)
        acc = sum(estimates) / float(len(estimates))
        accline = "Average difference: " + str(acc) + " degrees fahrenheit\n"
        logfile.write(accline)
    print("Done. Log file located at: " + outfile_name)

#parseData Function
#Read the .csv input file
#Populate a dictionary of date/avg temp
def parseData():
    with open(infile_name, 'rb') as csvfile:
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

            temp = row[3]
            for char in temp:
                if(char not in accept):
                    temp = temp.replace(char, '')
            if(temp != ""):
                temp = float(temp)
                dates_temps[f_date] = temp

#isLeap Function
#Helper function to determine whether a given year is a leap year
def isLeap(d):
    if(d.year % 4 == 0 and d.year % 100 != 0):
        return True
    elif(d.year % 400 == 0):
        return True
    else:
        return False

#findAvg Function
#The temperature imputation is done within this function
def findAvg(missing_date):
    #The list of temperatures for the missing year
    origTempRange = []

    #The years other than the missing one
    otherYears = []

    #The list of temperatures for the other years, same dates
    otherYearsTemps = []

    #The list of difference in temperatures
    #between the missing year and all other years
    diffList = []

    for i in range(-date_range, date_range+1):
        if(i == 0):
            continue
        origTempRange.append(dates_temps[missing_date + timedelta(days=i)])

    for i in dates_temps:
        if(i.month == missing_date.month
            and (i.day == missing_date.day or i.day == missing_date.day - 1)
            and i.year != missing_date.year):
            if(isLeap(i) == True):
                if(i.day != 28):
                    otherYears.append(i)
            else:
                otherYears.append(i)

    listOfDates = []
    for i in dates_temps:
        for j in otherYears:
            if(i == j):
                if(i >= date(1990, 1, 1) and i <= date(2004, 12, 31)):
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

    #Find the indices of the mins
    tempList = []
    for i in range(3):
        for j in avg:
            if(mins[i] == j):
                tempList.append(avg.index(j))
                break

    newList = []
    for i in tempList:
        newList.append(listOfDates[i])

    finalAns = 0
    for i in dates_temps:
        for j in newList:
            if(i == j):
                finalAns += dates_temps[i]
    finalAns = round(finalAns/3, 2)
    return finalAns

parseData()
runAnalysis()
