import soundcloud as sc
import pprint as pp 

client = sc.Client(client_id='7460ba6c0c64e2e019aeca796eb3a4f7'
													,client_secret = '1b005ace1bd8c5dff552faedaa99eb70'
													,username='Adusei'
											    ,password='Dinginator06')

#def get_my_favs():
all_of_my_favs = []

my_id = client.get('/me').id
print my_id

my_favorites_request = 'users/'+ str(my_id) +'/favorites'

my_favorites = client.get(my_favorites_request)
for my_favs in my_favorites:
		favs_dict = {}
		favs_dict['track_id']= my_favs.id
		favs_dict['title']= my_favs.title
		favs_dict['duration']= ( my_favs.duration ) / 600000.00 
		all_of_my_favs.append(favs_dict)

pp.pprint(all_of_my_favs)



#TRAINING DATA:
	# My Likes.. sounds that i like
	# Starting small... defining the prediction based off of time only.

# Sounds are tagged with things i like and I dont like..
# Predict if i like it.. or if i dont


