#!/usr/bin/env python
import numpy as np
import pylab as pl
import pandas as pd
import pprint as pp
  
from matplotlib.colors import ListedColormap

from sklearn import cross_validation as cv
from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.preprocessing import scale

data_url = 'https://raw.github.com/dzorlu/GADS/4c3ee79773d3c6024979e20d337ad2210be68ac9/data/wine.txt'

NUM_NBRS = 21
FOLDS = 10
RESULTS = []
CROSS_VAL_ARRAY = []


def process_data(data_src):
  header = ['label','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
  data = pd.read_csv(data_src,header=None,names=header)

  features = data.drop('label', 1)
  labels = data.label 

  #run_knn(features, labels, features,labels,1,5)
  #cross_val( features, labels, FOLDS ,NUM_NBRS)
  find_opt_k ( features, labels )

def cross_val(features, labels, num_folds, k):
    cv_results = {}
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True)

    for i, (train_index, test_index) in enumerate(kf):
      train_features = features.loc[train_index].dropna()
      train_labels = labels.loc[train_index].dropna()

      test_features = features.loc[test_index].dropna()
      test_labels = labels.loc[test_index].dropna()

      run_knn(train_features, train_labels,test_features, test_labels, i, k)

    avg_acc = sum(CROSS_VAL_ARRAY) / len(CROSS_VAL_ARRAY)

    cv_results['k'] = k
    cv_results['avg_acc'] = avg_acc
    RESULTS.append(cv_results)
    print cv_results

def find_opt_k(features,labels):
    CROSS_VAL_ARRAY = []
    nmbs =list(range(1,101))
    for nm in nmbs:
      if nm % 2 != 0:
        loop_ind = '\n'+ '=' * 20 + 'k: ' + str(nm) + '=' * 20 
        print loop_ind * 3 + '\n'
        cross_val (features, labels, FOLDS, nm)

def run_knn(train_features, train_labels,test_features, test_labels, iteration=None,k=None):
    clf = knn(n_neighbors = k)
    clf.fit(train_features, train_labels)

    acc = clf.score(test_features, test_labels)

    predicted_labels = clf.predict(test_features)
    cm = confusion_matrix(test_labels, predicted_labels)

    #print 'iteration:'.format(iteration)
    #print 'num_features = {0}'.format(num_features)
    #print 'k = {0}'.format(k)
    #print 'accuracy = {0} %\n'.format(round(100 * acc, 2))
    #print 'confusion matrix:\n', cm, '\n'

    CROSS_VAL_ARRAY.append(acc)

if __name__ == '__main__':
  process_data(data_url)
  pp.pprint(RESULTS)

#http://archive.ics.uci.edu/ml/datasets/Wine
#i) Fit a kNN algorithm. Perform cross-validation to pick the best value for k.
    # -> k = 9 
    # how do i balance a high accuracy for a low 
    # value of k given that when k approaches zero
    # the model becomes over fit?
    
#ii) Perform cross-validation to pick the best model between logistic regression and kNN. Does the answer change when you use different CV technique?


