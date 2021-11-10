#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import glob
import time
import datetime
import numpy as np

# Treiberinstallation
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Temperatursensor initialisieren 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_rom():
	name_file=device_folder+'/name'
	f = open(name_file,'r')
	return f.readline()

# Sensor Temperatur lesen lassen
def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# Temperatur auslesen
def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c
	

# Ausgabe
hMaxTemp = -20.8
hMinTemp = 30.7
dMaxTemp = -21.2
dMinTemp = 31.3
#
# define min and max array for 24 hours
#
#hourlyMinMax = [[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
#daylyMinMax = [[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
#                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#                [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


hourlyMinMax = np.loadtxt("scratch.txt").reshape(3, 24)
daylyMinMax = np.loadtxt("scratchDay.txt").reshape(3, 31)

print("Starting with this vanlues from scratch.txt for hourly values\n")
print(hourlyMinMax)

print("Starting with this vanlues from scratchDay.txt for dayly values\n")
print(daylyMinMax)

dt = datetime.datetime.now()
#day = dt.day
day = dt.day
hour = dt.hour
minute = dt.hour
while True:
    dt = datetime.datetime.now()
#    print(day, dt.minute)
    if day != dt.day:
#        New day
        
        print("New day", day)       
        print("Max temp this day is: ", dMaxTemp)
        daylyMinMax [1] [day - 1] = dMaxTemp
        print("Min temp this day is: ", dMinTemp)
        daylyMinMax [2] [day - 1] = dMinTemp
        
        day = dt.day
        
        a_file = open("scratchDay.txt", "w")
        for row in daylyMinMax:
           np.savetxt(a_file, row)

        a_file.close()
 
# Set new min max for day
        
        dMaxTemp = -30.4
        dMinTemp = 90.6
        
    if hour != dt.hour:
#        New hour
        
        print("New hour", dt.hour)        
        print("Max temp this hour is: ", hMaxTemp)
        hourlyMinMax [1] [hour] = hMaxTemp
        print("Min temp this hour is: ", hMinTemp)
        hourlyMinMax [2] [hour] = hMinTemp
        
        hour = dt.hour
        
        print(hourlyMinMax)
        print("Saving matrix to scratch.txt \n")
        a_file = open("scratch.txt", "w")
        for row in hourlyMinMax:
           np.savetxt(a_file, row)

        a_file.close()

        

# Set new min max for hour

        hMaxTemp = -30.1
        hMinTemp = 92.1
     

    curTemp = read_temp()

    if curTemp > dMaxTemp:
        dMaxTemp = curTemp
    if curTemp < dMinTemp:
        dMinTemp = curTemp
    
    if curTemp > hMaxTemp:
        hMaxTemp = curTemp
    if curTemp < hMinTemp:
        hMinTemp = curTemp
    
    print(dt)
    print(' %3.3f *C'% curTemp, dMinTemp, dMaxTemp, hMinTemp, hMaxTemp)
    
# open log file for write

    f = open("templog.log","a")
    tempString = str(curTemp) + " " + str(dMinTemp) +" " + str(dMaxTemp) + " " + str(hMinTemp) + " " + str(hMaxTemp)
    f.write("Temperature = " + tempString + "\n")
    f.close()
    time.sleep(60)
