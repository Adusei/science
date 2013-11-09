import urllib2
import csv
import json
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import os
import random
from math import radians, cos, sin, asin, sqrt

#source: http://tinyurl.com/q2kzam2
#source: http://tinyurl.com/ndn34u4
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

print 'generating random lat/long to simulate mobile request...'

Location = r'data/citibike_parsed.csv' #chicken and egg problem here...
inp = read_csv(Location,header=0) 

mx_value = inp['latitude'].max()
mx_value = inp['longitude'].max()

mx_lat = inp['latitude'].max()
mn_lat = inp['latitude'].min()
mx_lon = inp['longitude'].max()
mn_lon = inp['longitude'].min()

lat_request = random.uniform(mx_lat, mn_lat)
lon_request = random.uniform(mx_lon, mn_lon)

print 'request-lat:' + str(lat_request)
print 'request-lon:' + str(lon_request)

#create a python script that parses the original citibike.json into a file like citibike.csv

response = urllib2.urlopen('http://citibikenyc.com/stations/json/')
citibike_json = response.read()

citibike_json = json.loads(citibike_json)

writer = csv.writer(open('data/citibike_parsed.csv', 'wb'))
writer.writerow(["id", "stationName", "availableDocks", "totalDocks", "latitude","longitude","statusValue","availableBikes","stAddress1","city","postalCode","location","pct_available","distance_from_request"])

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
		##
	avail = station["availableBikes"]
	total = station["totalDocks"]
	avail_pct = float(avail) / float(total)
	csv_line.append(avail_pct)
		##
	station_lat = station["latitude"]
	station_lon = station["longitude"]
	distance_from_request = haversine(lat_request, lon_request, station_lat, station_lon) 
	csv_line.append(distance_from_request)

	writer.writerow(csv_line)
'''
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
'''

print 'INCOMING REQUEST FROM: ' + str(lat_request) + ',' + str(lon_request)

print 'excuse me operator.. can you please tell me what the closest citi bike location is??'

mn_dist = inp['distance_from_request'].min()
mn_dist_name = inp['stationName'][inp['distance_from_request'] == mn_dist].values

print 'the closest station to your location is ' + mn_dist_name + ' which is ' + str(mn_dist) +  ' km away... have fun!'

# suppose you have an incoming stream of messages
# containing lat/lon info. how could you determine
# which station is the closest for each message?


# suppose you wanted to create a visualization
# to represent this dataset. what fields would
# you want to use? why? how would you use them?

