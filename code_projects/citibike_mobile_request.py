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

Location = r'data/citibike_parsed.csv'
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

print 'what station is closest to the request?'

#bk_to_bxv = haversine(40.6944, -73.9906,40.9400, -73.8261) #my apt to bronxville
result = haversine(lat_request, lon_request, mx_lat, mx_lon) 

print 'it is ' + str(result) + ' km from the request to some station..'


