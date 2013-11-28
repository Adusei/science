import soundcloud

# create client object with app credentials
#client = Soundcloud.new(:client_id => '607f0d77719587d3fab7f79c54a32e80',
#                        :client_secret => 'd2a404de1518945ddec8127334952ff1',
#                        :redirect_uri => 'http://localhost:3000/')


client = soundcloud.Client(client_id='7460ba6c0c64e2e019aeca796eb3a4f7'
													,client_secret = '1b005ace1bd8c5dff552faedaa99eb70')

# find all sounds of buskers licensed under 'creative commons share alike'
tracks = client.get('/tracks', q='thugfucker')

#duration => {:from => 3600000} , :limit => 10 

#print type(tracks)

for t in tracks:
		print t.id
		print t.description



#TRAINING DATA:
	# My Likes.. sounds that i like
	# Starting small... defining the prediction based off of time only.

# Sounds are tagged with things i like and I dont like..
# Predict if i like it.. or if i dont


