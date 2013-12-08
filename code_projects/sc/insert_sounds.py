import MySQLdb as mysql
import pprint as pp

import recommender_test as rt

SOUND_ID = 93062339

db = mysql.connect(host="localhost",user="root",db="mix")

def insert_sound(sc_sound_id,title):
	title = title.replace("'","")
	x = db.cursor()
	exists_clause = 'select (1) from listen_sound where sc_id = ' + str(sc_sound_id)

	if not x.execute(exists_clause): 
		x.execute("""INSERT INTO 	listen_sound (sc_id, title) VALUES (%s,%s)""",(sc_sound_id,title))
	
		db.commit()

def inssert_may_favs():
	myfavs = rt.get_favs_by_user(6596434)
	for f in myfavs:
		f_id = f["track_id"]
		f_title = f["title"]
		insert_sound(f_id,f_title)
		pp.pprint(f)


if __name__ == '__main__':
	insert_sound(93062339,"Flombo at Robot Heart")
	inssert_may_favs()