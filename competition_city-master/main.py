"""
Author      :   Muhammad Nabil Muhammad
Date        :   25th November 2018
Description :   Labeling points according to which city it belongs or dont belong to any city -None- and exporting
                CSV file with points data added with 4th column about its location
"""

import csv
import matplotlib.pyplot as plt

locations = list()
names = list()
xCoordinates = list()
yCoordinates = list()
points = list()


# extracting data from cities.csv into lists

def parsingcities():
    cities = open('cities.csv', 'r')
    reader = csv.DictReader(cities)
    for line in reader:
        locations.append(list(line.values()))
        names.append(line['Name'])
        xCoordinates.append((line['TopLeft_X'], line['BottomRight_X']))
        yCoordinates.append((line['TopLeft_Y'], line['BottomRight_Y']))
    return names, xCoordinates, yCoordinates


# extracting data from points.csv into points list

def parsingpoints():
    pointcsv = open('points.csv', 'r')
    reader = csv.DictReader(pointcsv)
    for line in reader:
        points.append([line['ID'], line['X'], line['Y']])
    return points


# Checking a point in range with which city X coordinates

def betweenx(pointx, cityx):
    if pointx >= int(cityx[0]) and pointx <= int(cityx[1]):
        return True
    return False


# after using betweenx function, this function can only be executed after betweenx return True. it check if the selected
# city by its X could also be in range of its Y coordinates. if so, then it belong to this city

def betweeny(pointy, cityy):
    if pointy >= int(cityy[0]) and int(cityy[1]) >= pointy:
        return True
    return False


# searching for each point to find which city it belong or None by using betweenx , betweenty

def searching():
    pointsposition = list()

    for point in points:
        found = False
        for city, x in enumerate(xCoordinates, 0):
            if betweenx(int(point[1]), xCoordinates[city]):
                if betweeny(int(point[2]), yCoordinates[city]):
                    pointsposition.append(names[city])
                    found = True
                    break
        if not found:
            pointsposition.append('None')
    return pointsposition


# outputcsv is output function to add 4th column to points.csv and produce output_points.csv file

def outputcsv(pointsposition):
    points = open('points.csv', 'r')
    output = open('output_points.csv', 'w')
    csvreader = csv.DictReader(points)
    fieldnames = csvreader.fieldnames + ['Location']
    csvwriter = csv.DictWriter(output, fieldnames)
    csvwriter.writeheader()
    for position, line in enumerate(csvreader, 0):
        line.update(dict(Location=pointsposition[position]))
        csvwriter.writerow(line)


# plotting function is to plot the whole map and draw cities and points

def plotting():
    plt.axes()
    for location in locations:
        x = list(map(int, [location[1], location[3], location[3], location[1], location[1]]))
        y = list(map(int, [location[2], location[2], location[4], location[4], location[2]]))
        plt.plot(x, y)
    for point in points:
        plt.plot(int(point[1]), int(point[2]), markersize=8, marker='*')
    plt.show()


# parsing data

names, xCoordinates, yCoordinates = parsingcities()
points = parsingpoints()

# searching and produce output file

outputcsv(searching())

# plotting the map

plotting()
