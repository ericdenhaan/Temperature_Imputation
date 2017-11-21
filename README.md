# README #

4310 Project - Missing Temperature Imputation
Dawson Meyer and Eric Den Haan

Dataset: Daily Summaries for Great Falls, MT 1990-2004
https://www.ncdc.noaa.gov/cdo-web/datasets#GHCND

Eric:

Take NOAA .csv file as input, return dictionary of dates (YYYY-MM-DD) and avg. daily temperatures
Gather input from user (date to impute, days before and after to consider)
Provide output to user

Dawson:

Take a date and number of days before and after to consider
Get the "distance" from the date in the given year, calculate the average "distance" for the date range
Pick the three lowest average distances, return the list of years with these lowest distances

Unassigned:

Take a list of 3 years as input as well as a missing date
Calculate the average value for the missing date
Compare with actual value for the missing date and determine accuracy, return these values
