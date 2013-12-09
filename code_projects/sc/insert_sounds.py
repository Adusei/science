import MySQLdb as mysql
import pprint as pp
import soundcloud as sc 
import pprint as pp

import recommender_test as rt

client = sc.Client(client_id='7460ba6c0c64e2e019aeca796eb3a4f7'
                  ,client_secret = '1b005ace1bd8c5dff552faedaa99eb70'
                  ,username='Adusei'
                  ,password='Dinginator06')

db = mysql.connect(host="localhost",user="root",db="mix")

def insert_sound(sc_sound_id,title):
	title = title.replace("'","")
	x = db.cursor()
	exists_clause = 'select (1) from listen_sound where sc_id = ' + str(sc_sound_id)

	if not x.execute(exists_clause): 
		x.execute("""INSERT INTO 	listen_sound (sc_id, title,jd_fav_flag,jd_follows_like_count) VALUES (%s,%s,%s,%s)""",(sc_sound_id,title,True,-1))
	
		db.commit()
		
def insert_user_favs(user_id):
	myfavs = rt.get_favs_by_user(user_id)
	for f in myfavs:
		if f["duration"] > 60.00:
			f_id = f["track_id"]
			f_title = f["title"]
			insert_sound(f_id,f_title)
			pp.pprint(f)

def get_followed_users_by_user(user_id):
	user_list = []
	response = 'users/'+ str(user_id) +'/followings'
	user_followings = client.get(response,limit=1000)

	return user_followings

def populate_a_bunch_of_sounds():
	users = get_followed_users_by_user(6596434)
	for i,(u) in enumerate(users):
		if i < 20:
			insert_user_favs(u.id)
			print u.id



if __name__ == '__main__':
	populate_a_bunch_of_sounds()
	# insert_may_favs()
	# insert_followed_user_favs(6596434)

