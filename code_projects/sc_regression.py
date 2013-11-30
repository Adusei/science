import soundcloud as sc
import pprint as pp
import pandas as pd
import numpy as np
import random as rd
import datetime as dt
import json


from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import confusion_matrix
from sklearn import cross_validation as cv

TRAIN_PCT = 0.7

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

  #a = dt.datetime(sc_track_object.created_at)
  #b = dt.datetime(2013,12,31,23,59,59)
  #(b-a).total_seconds()


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

def get_my_favs():
  #http://api.soundcloud.com/tracks/92518013.json?client_id=7460ba6c0c64e2e019aeca796eb3a4f7
  all_of_my_favs = []

  my_id = client.get('/me').id
  response = 'users/'+ str(my_id) +'/favorites'
  my_favorites = client.get(response)

  for f in my_favorites:
    favs_dict = create_track_dict(f)
    all_of_my_favs.append(favs_dict)

  return all_of_my_favs


def get_random_tracks(limit_input):
  all_random_tracks = []

  tracks = client.get('/tracks', limit=limit_input)

  for track in tracks: # make this modular...
    tracks_dict = create_track_dict(track)
    all_random_tracks.append(tracks_dict)

  return all_random_tracks

def prepare_data(control_data, experiment_data):

  all_data = []

  for x in control_data:
    x['label'] = 1
    all_data.append(x)

  for y in experiment_data:
    y['label'] = 0
    all_data.append(y)

  cntrl_df = pd.DataFrame.from_records(control_data).set_index('track_id')
  expr_df = pd.DataFrame.from_records(experiment_data).set_index('track_id')
  
  all_data = cntrl_df.append(expr_df)

  print str(len(all_data)) + ' <--- data length'
  print str(len(cntrl_df)) + ' <--- control length'
  print str(len(expr_df)) + ' <--- expr length'

  all_data = all_data.reindex(np.random.permutation(all_data.index))

  return all_data

def kfolds(features, labels, num_folds):
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True ,random_state=0, indices=False)
    return kf

def run_logistic_regression(train_x, train_y, test_x, test_y, iteration):
  model = LR()
  model.fit(train_x, train_y)

   # get model outputs
  inputs = map(str, train_x.columns.format())
  coeffs = model.coef_[0]
  accuracy = model.score(test_x, test_y)

  predicted_y = model.predict(test_x)
  cm = confusion_matrix(test_y, predicted_y)

  print 'inputs = {0}'.format(inputs)
  print 'coeffs = {0}'.format(coeffs)
  print 'accuracy = {0}'.format(accuracy)     # mean 0/1 loss
  print 'confusion matrix:\n', cm, '\n'


def cross_validate(data,num_folds=10):
    data = data.drop('title',1)
    data = data.drop('tags',1)


    features = data.drop('label', 1)
    labels = data.label

    num_recs = len(data)
    print num_recs
    print '^ number of records'    
    kf = kfolds(features, labels, num_folds)

    for i, (train_index, test_index) in enumerate(kf):

      loop_ind = '\n'+ '=' * 20 + 'Loop Number: ' + str(i) + '=' * 20 

      print loop_ind * 3 + '\n'

      train_features = features.loc[train_index].dropna()
      train_labels = labels.loc[train_index].dropna()

      test_features = features.loc[test_index].dropna()
      test_labels = labels.loc[test_index].dropna()

      run_logistic_regression(train_features, train_labels, test_features, test_labels, i)


if __name__ == '__main__':
  expr  =  get_random_tracks(180)
  cntrl =  get_my_favs()
  #get_my_favs()
  tracks =  prepare_data(cntrl, expr)
  cross_validate(tracks)

# soundcloud app uri: py_ml_yp
# Predict if i like it.. or if i dont


