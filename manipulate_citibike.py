import urllib2
import csv
import json

response = urllib2.urlopen('http://citibikenyc.com/stations/json/')
citibike_json = response.read()

citibike_json = json.loads(citibike_json)

#f = write(open("test.csv", "wb+"))
#f = csv.write(open("test.csv", "wb+"))

# Write CSV Header, If you dont need that, remove this line

#writer = csv.writer(open("/path/to/my/csv/file", 'w'))
writer = csv.writer(open('citibike_parsed.csv', 'wb'))
writer.writerow(["id", "stationName", "availableDocks", "totalDocks", "latitude","longitude","statusValue","availableBikes","stAddress1","city","postalCode","location"])

#for (k,v) in citibike_json:
for k,v in citibike_json.items():
    if k == 'stationBeanList':
    	stations = v

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
	writer.writerow(csv_line)
	



	