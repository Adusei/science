import json
import urllib
import MySQLdb as mysql
import string

API_KEY = "AIzaSyCXG-AcgddTtoqijaTzOs8IiE97qsl8gqI"
service_url = 'https://www.googleapis.com/freebase/v1/mqlread'

def get_genres(con):
	# https://developers.google.com/freebase/v1/mql-overview

	query =     [{"name":None,"mid":None,"type": "/music/genre","limit": 10000}]

	params = {'query': json.dumps(query),'key': API_KEY}

	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	for genre in response['result']:
		m_id =  genre['mid']
		genre_name = genre['name']
		if genre_name is not None:
			tokens = string.split(genre_name, ' ')		
			for token in tokens:
				if token.lower() == 'house' or token.lower() == 'techno':
					insert_genre(m_id,genre_name,con)

def insert_genre(mid, name, con):
	x = con.cursor()

	exists_clause = "select (1) from genres where m_id  = '" + str(mid) + "' limit 1"

	if x.execute(exists_clause): 
		x.execute("""INSERT INTO genres (m_id, genre_name) VALUES (%s,%s)""",(mid,name))
		con.commit()

def connect_to_db():
	conn = mysql.connect(host="localhost",user="root",db="sandbox")
	return conn

if __name__ == '__main__':
	conn = connect_to_db()
	get_genres(conn)


# create table genres
# (
# 	genre_id INT PRIMARY KEY AUTO_INCREMENT
# 	,m_id NVARCHAR(10)
# 	,genre_name NVARCHAR(255)
# );