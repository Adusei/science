import soundcloud as sc
import pprint as pp
import pandas as pd
import numpy as np
import random as rd


from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import confusion_matrix
from sklearn import cross_validation as cv

TRAIN_PCT = 0.7

client = sc.Client(client_id='7460ba6c0c64e2e019aeca796eb3a4f7'
                  ,client_secret = '1b005ace1bd8c5dff552faedaa99eb70'
                  ,username='Adusei'
                  ,password='Dinginator06')

def get_my_favs():
  all_of_my_favs = []

  my_id = client.get('/me').id
  
  my_favorites_request = 'users/'+ str(my_id) +'/favorites'

  my_favorites = client.get(my_favorites_request)

  for my_fav_instance in my_favorites:
      favs_dict = {}
      favs_dict['track_id']= my_fav_instance.id
      #favs_dict['title']= my_fav_instance.title
      #favs_dict['random_number']= rd.uniform(0,1)
      #favs_dict['playback_count'] = my_fav_instance.playback_count
      favs_dict['duration']= ( my_fav_instance.duration ) / 60000.00 #minutes
      all_of_my_favs.append(favs_dict)
      pp.pprint
      #pp.pprint(vars(my_fav_instance))

  return all_of_my_favs

  #pp.pprint(all_of_my_favs)

def get_random_tracks(limit_input):
  all_random_tracks = []

  tracks = client.get('/tracks', limit=limit_input)

  for track in tracks: # make this modular...
    tracks_dict = {}
    tracks_dict['track_id']= track.id
    #tracks_dict['title']= track.title
    #tracks_dict['random_number']= rd.uniform(0,1)
    #tracks_dict['playback_count'] = track.playback_count
    tracks_dict['duration']= ( track.duration ) / 60000.00 #minutes
    all_random_tracks.append(tracks_dict)

  #pp.pprint(all_random_tracks)

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

  return all_data


def kfolds(features, labels, num_folds):
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True,random_state=0)
    return kf

def run_logistic_regression(data):#(train_x, train_y, text_x, text_y):#,iteration):
  data = data.reindex(np.random.permutation(data.index))

  split_pt = int(TRAIN_PCT * len(data))

  train_x = data[:split_pt].drop('label', 1)      # training set features
  train_y = data[:split_pt].label                 # training set target

  test_x = data[split_pt:].drop('label', 1)       # test set features
  test_y = data[split_pt:].label                  # test set target

  # initialize model & perform fit
  model = LR()                        # model is an "instance" of the class LR
  model.fit(train_x, train_y)         # perform model fit ("in place")

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
    #data = data.drop('title',1)
    data = data.reindex(np.random.permutation(data.index))

    features = data.drop('label',1)
    labels = data.label 

    print '===' * 20
    print 'DATA' 
    print '===' * 20

    print data

    print '===' * 20
    print 'FEATURES' 
    print '===' * 20
    
    print features

    print '===' * 20
    print 'LABELS' 
    print '===' * 20

    print labels

    print '< len feathres'
    print features.shape 

    '< len lables'
    print labels.shape 

    run_logistic_regression(features, labels, features, labels)

    '''
    num_recs = len(data)
    kf = kfolds(features, labels, num_folds)


    for i, (train_index, test_index) in enumerate(kf):

         loop_ind = '\n'+ '=' * 20 + 'Loop Number: ' + str(i) + '=' * 20 

         print loop_ind * 3 + '\n'

         train_features = features.loc[train_index].dropna()
         train_labels = labels.loc[train_index].dropna()

         test_features = features.loc[test_index].dropna()
         test_labels = labels.loc[test_index].dropna()

         print str(test_labels) + '<test labels'
         print str(train_labels) + '<train labels'
         run_logistic_regression(train_features, train_labels, test_features, test_labels, i)
  '''
if __name__ == '__main__':
  expr  =  get_random_tracks(50)
  cntrl =  get_my_favs()
  tracks =  prepare_data(cntrl, expr)
  #cross_validate(tracks)
  run_logistic_regression(tracks)

# soundcloud app uri: py_ml_yp

#TRAINING DATA:
  # My Likes.. sounds that i like
  # Starting small... defining the prediction based off of time only.

# Sounds are tagged with things i like and I dont like..
# Predict if i like it.. or if i dont


