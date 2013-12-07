import json
import urllib
import MySQLdb as mysql
import string
import pprint

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

	if not x.execute(exists_clause): 
		x.execute("""INSERT INTO genres (m_id, genre_name) VALUES (%s,%s)""",(mid,name))
		con.commit()


def get_artists_by_genres(genre_m_id, conn):
	query = [{
		  "genre": {
		    "mid": genre_m_id
		  },
		  "mid": None,
		  "name": None,
		  "type": "/music/artist",
		  "limit": 300
		}]
	params = {'query': json.dumps(query),'key': API_KEY}

	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	for artist in response['result']:
		artist_mid = artist['mid']
		artist_name = artist['name']

		insert_artist(artist_mid, artist_name, conn)
		# artist_id = 
		# insert_artist_to_genre(artist_id, genre_id, conn)

def insert_artist(mid, name, con):

	x = con.cursor()

	exists_clause = "select (1) from artists where m_id  = '" + str(mid) + "' limit 1"

	if not x.execute(exists_clause): 
		print mid
		print name
		x.execute("""INSERT INTO artists (m_id, artist_name) VALUES (%s,%s)""",(mid,name))
		con.commit()

def insert_artist_to_genre(artist_id, genre_id, con):
	data = cursor.fetchall()
	for row in data :
	    do stuff

# 	x = con.cursor()

# 	exists_clause = "select (1) from artist_to_genre where artist_id = and genre_id = "

# 	if x.execute(exists_clause): 
# 		x.execute("""INSERT INTO genres (m_id, artist_name) VALUES (%s,%s)""",(mid,name))
# 		con.commit()


# def get_genre_relations(genre_id):


def connect_to_db():
	conn = mysql.connect(host="localhost",user="root",db="sandbox")
	return conn

if __name__ == '__main__':
	conn = connect_to_db()
	# get_genres(conn)
	get_artists_by_genres("/m/01zh00",conn)
