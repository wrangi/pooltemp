from flask import Flask, json, url_for
import datetime
import time
import numpy as np



# Wait for things to start
time.sleep(60)

api = Flask(__name__)

api.config["DEBUG"] = True

# Send hourly Max and min

@api.route('/climateh', methods=['GET'])
def get_climateh():
    
# Get data from scratch file

    hourlyMinMax = np.loadtxt("scratch.txt").reshape(3, 24)
    
    dayMax = -20
    dayMin = 40
    hotestHour = 0
    coolestHour = 0
    for lHour in range (0, 24, 1):
        if hourlyMinMax[1][lHour] > dayMax:
            dayMax = hourlyMinMax[1][lHour]
            hotestHour = lHour
        if hourlyMinMax[2][lHour] < dayMin:
            dayMin = hourlyMinMax[2][lHour]
            coolestHour = lHour
    
    output = "<!DOCTYPE html><html><head><title>Temperatur i poolen timmar</title></head><body><h1>Temperatur log i poolen timmar</h1><table style=\"width:100%\"> \
<tr> <td>Timme: </td> <td>Max temperatur</td><td>Min temperatur</td></tr>"
    for lHour in range (0, 24, 1):
        output = output + "<tr><td>" + str(lHour) + "</td>"
        if hotestHour == lHour:
            output = output + "<td style=\"background-color:#FF0000\">"
        else:
            output = output + "<td>"
        if hourlyMinMax[1][lHour] > 0:
            output = output + "+"
        output = output + str(hourlyMinMax[1][lHour]) + "</td>"
        if coolestHour == lHour:
            output = output + "<td style=\"background-color:#13E0FE\">"
        else:            
            output = output + "<td>"
        if hourlyMinMax[1][lHour] > 0:
            output = output + "+"
        output = output + str(hourlyMinMax[2][lHour]) + "</td></tr>"    
    output = output + "</table>"
    
    dt = datetime.datetime.now() 
    d = dt.date()
    sD = str(d)
    
    t = dt.time()
    sTimeLong = str(t)
    sT = sTimeLong[0:8]
    
    output = output + "Datum: " + sD + "  "
    
    output = output + "Klockan: " + sT
    
    output = output + "</body></html>"
    

    print(output)
    
#  return json.dumps(companies)
    return output

# Send dayly Max and min

@api.route('/climated', methods=['GET'])
def get_climated():
    
# Get data from scratch file

    daylyMinMax = np.loadtxt("scratchDay.txt").reshape(3, 31)
    
    monthMax = -20
    monthMin = 40
    hotestDay = 0
    coolestDay = 0
    for lDate in range (1, 31, 1):
        if daylyMinMax[1][lDate - 1] > monthMax:
            monthMax = daylyMinMax[1][lDate]
            hotestDay = lDate
        if daylyMinMax[2][lDate - 1] < monthMin:
            monthMin = daylyMinMax[2][lDate - 1]
            coolestDay = lDate
    
    output = "<!DOCTYPE html><html><head><title>Temperatur i poolen dagar</title></head><body><h1>Temperatur log i poolen dagar</h1><table style=\"width:100%\"> \
<tr> <td>Dag: </td> <td>Max temperatur</td><td>Min temperatur</td></tr>"
    for lDate in range (1, 32, 1):
        output = output + "<tr><td>" + str(lDate) + "</td>"
        if hotestDay == lDate:
            output = output + "<td style=\"background-color:#FF0000\">"
        else:
            output = output + "<td>"
        output = output + str(daylyMinMax[1][lDate - 1]) + "</td>"
        if coolestDay == lDate:
            output = output + "<td style=\"background-color:#13E0FE\">"
        else:
            output = output + "<td>"
        output = output + str(daylyMinMax[2][lDate - 1]) + "</td></tr>"    
    output = output + "</table>"
    
    dt = datetime.datetime.now() 
    d = dt.date()
    sD = str(d)
    
    t = dt.time()
    sTimeLong = str(t)
    sT = sTimeLong[0:8]
    
    output = output + "Datum: " + sD + "  "
    
    output = output + "Klockan: " + sT
    
    output = output + "</body></html>"
    

    print(output)
    
#  return json.dumps(companies)
    return output

api.run(host="192.168.0.168",port=5004)
