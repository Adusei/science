import urllib2
import csv
import json
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import os


#create a python script that parses the original citibike.json into a file like citibike.csv

response = urllib2.urlopen('http://citibikenyc.com/stations/json/')
citibike_json = response.read()

citibike_json = json.loads(citibike_json)

writer = csv.writer(open('data/citibike_parsed.csv', 'wb'))
writer.writerow(["id", "stationName", "availableDocks", "totalDocks", "latitude","longitude","statusValue","availableBikes","stAddress1","city","postalCode","location","pct_available"])

for k,v in citibike_json.items():
    if k == 'stationBeanList':
    	stations = v
    elif k == 'executionTime':
    	time_of_request = v

for station in stations:
	csv_line = []
	csv_line.append(station["id"])
	csv_line.append(station["stationName"])
	csv_line.append(station["availableDocks"])
	csv_line.append(station["totalDocks"])
	csv_line.append(station["latitude"])
	csv_line.append(station["longitude"])
	csv_line.append(station["statusValue"])
	#csv_line.append(station["In Service"]) # KeyError: 'In Service'
	csv_line.append(station["availableBikes"])
	csv_line.append(station["stAddress1"])
	csv_line.append(station["city"])
	csv_line.append(station["postalCode"])
	csv_line.append(station["location"])

	avail = station["availableBikes"]
	total = station["totalDocks"]
	avail_pct = float(avail) / float(total)

	csv_line.append(avail_pct)

	writer.writerow(csv_line)

print 'which station has the most total spots?'


Location = r'data/citibike_parsed.csv'
inp = read_csv(Location,header=0)
#print inp
#print inp.dtypes
#inp['id'].plot()
mx_value = inp['totalDocks'].max()
mx_name = inp['stationName'][inp['totalDocks'] == mx_value].values

print 'I think it is... ' + mx_name + ' with... ' + str(mx_value)

print 'which station has the highest pct of bikes available (at the time this file was created)?'

mx_pct = inp['pct_available'].max()
mn_pct = inp['pct_available'].min()
mx_pct_name = inp['stationName'][inp['pct_available'] == mx_pct].values
mn_pct_name = inp['stationName'][inp['pct_available'] == mn_pct].values

print 'I think it is... ' + mx_pct_name + ' with... ' + str(mx_pct) + ' at... ' + time_of_request

#suppose you wanted to create a visualization to represent this dataset. what fields would you want to use? why? how would you use them?
#suppose you have an incoming stream of messages containing lat/lon info. how could you determine which station is the closest for each message?

