import soundcloud as sc
import MySQLdb as mysql
import pprint as pp
import collections as cl
import operator as op
from dateutil import parser as date_parser
import datetime as dt

import nltk.classify
from nltk import NaiveBayesClassifier

client = sc.Client(client_id='7460ba6c0c64e2e019aeca796eb3a4f7'
                  ,client_secret = '1b005ace1bd8c5dff552faedaa99eb70'
                  ,username='Adusei'
                  ,password='Dinginator06')

def create_track_dict(sc_track_object):
  track_dict = {}
  track_dict['track_id']= sc_track_object.id
  track_dict['title']= sc_track_object.title
  track_dict['tags'] = sc_track_object.tag_list
  track_dict['duration']= ( sc_track_object.duration ) / 60000.00 #minutes
  track_dict['user_id']= sc_track_object.user_id

  a = sc_track_object.created_at
  a = date_parser.parse(a)
  a = a.replace(tzinfo=None)
  b = dt.datetime.now()
  b = b.replace(tzinfo=None)

  diff = (b-a).total_seconds() / 86400.00

  track_dict['day_since_release'] = diff

  try:
     fc = sc_track_object.favoritings_count
  except AttributeError:
     fc = -1

  track_dict['favs_count'] = fc

  try:
     pc = sc_track_object.favoritings_count
  except AttributeError:
     pc = -1

  track_dict['play_count'] = pc
  
  return track_dict

def get_favs_by_user(user_id):
  all_favs = []

  response = 'users/'+ str(user_id) +'/favorites'
  my_favorites = client.get(response,limit=1000)

  for f in my_favorites:
    favs_dict = create_track_dict(f)
    all_favs.append(favs_dict)

  return all_favs

def get_ngams_by_user (user_id):

  user_ngram_fdist = cl.defaultdict(int)
  my_favs = get_favs_by_user(user_id)

  for fav in my_favs:
    title =  fav['title']
    tag_list = fav['tags']
    user_id = fav['user_id'] # Not sure how i want to deal with this

    tag_list = tag_list.replace('"', '').lower()
    title = title.lower()

    title_tokens = nltk.word_tokenize(title)
    tag_tokens = nltk.word_tokenize(tag_list)

    tmp_tokens = title_tokens + tag_tokens

    bgs = nltk.bigrams(tmp_tokens)
    bg_fd = nltk.FreqDist(bgs)
    for ngram,freq in bg_fd.items():  
      ngram_str = ngram[0].encode('utf-8') + ' ' + ngram[1].encode('utf-8')
      user_ngram_fdist[ngram_str] += 1
      
  sorted_ngrams = sorted(user_ngram_fdist.iteritems(), key=op.itemgetter(1))  

  return sorted_ngrams

def find_follower_likes(user_id):
  all_tracks = cl.defaultdict(int)

  favorites  = 'users/'+ str(user_id) +'/favorites'
  user_favorites = client.get(favorites,limit=1000)

  response = 'users/'+ str(user_id) +'/followings'
  user_followings = client.get(response,limit=1000)

  for f in user_followings:
    print 'USER:  ' + f.username
    followed_user_id = f.id
    user_favs = get_favs_by_user(followed_user_id)
    for track in user_favs:
      if track['duration'] > 60.0:
        track_tuple = (track['track_id'],track['title'])
        all_tracks[track_tuple] += 1
        print track_tuple

  # remove favorites that current user also has as a favorite

  sorted_tracks = sorted(all_tracks.iteritems(), key=op.itemgetter(1))  

  pp.pprint(sorted_tracks)
  return sorted_tracks

if __name__ == "__main__":
  # get_ngams_by_user(6596434) #me
  find_follower_likes(6596434)
    # tj 3105250
    # yoshi 12772525

  # http://api.soundcloud.com/resolv
  # e.json?url=https://soundcloud.co
  # m/dteej&client_id=7460ba6c0c64e2
  # e019aeca796eb3a4f7



# the idea about a weighted graph
# in the way that "better" users
# titlt the graph in their favor
 
