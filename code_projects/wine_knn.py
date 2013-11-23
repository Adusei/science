#!/usr/bin/env python
import numpy as np
import pylab as pl
import pandas as pd

from matplotlib.colors import ListedColormap

from sklearn import cross_validation as cv
from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.preprocessing import scale

data_url = 'https://raw.github.com/dzorlu/GADS/4c3ee79773d3c6024979e20d337ad2210be68ac9/data/wine.txt'

NUM_NBRS = 7
MESH_SIZE = 0.02
FOLDS = 5


def process_data(data_src):
  header = ['label','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
  data = pd.read_csv(data_src,header=None,names=header)

  features = data.drop('label', 1)
  labels = data.label 

  #cross_val( features, labels, FOLDS ,NUM_NBRS)
  find_opt_k ( features, labels )

def cross_val(features, labels, num_folds, k):
    acc_array = []
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True)

    for i, (train_index, test_index) in enumerate(kf):

      loop_ind = '\n'+ '=' * 20 + 'Loop Number: ' + str(i) + '=' * 20 

      print loop_ind * 3 + '\n'

      train_features = features.loc[train_index].dropna()
      train_labels = labels.loc[train_index].dropna()

      test_features = features.loc[test_index].dropna()
      test_labels = labels.loc[test_index].dropna()

      run_knn(train_features, train_labels,test_features, test_labels, i, k)

def find_opt_k(features,labels):
    nmbs = [1,2,3,4,5,6,7,8,9,10]
    for nm in nmbs:
      if nm % 2 != 0:
        cross_val (features, labels, FOLDS, nm)

def run_knn(train_features, train_labels,test_features, test_labels, iteration,k):

    clf = knn(n_neighbors = k)
    clf.fit(train_features, train_labels)

    # get accuracy (predictions made internally)
    acc = clf.score(test_features, test_labels)

    # get conf matrix (requires predicted labels)
    predicted_labels = clf.predict(test_features)
    cm = confusion_matrix(test_labels, predicted_labels)

    print 'iteration:'.format(iteration)
    print 'k = {0}'.format(k)
    #print 'num_features = {0}'.format(num_features)
    print 'accuracy = {0} %\n'.format(round(100 * acc, 2))
    print 'confusion matrix:\n', cm, '\n'

if __name__ == '__main__':
  process_data(data_url)
  #find_opt_k()


#http://archive.ics.uci.edu/ml/datasets/Wine
#i) Fit a kNN algorithm. Perform cross-validation to pick the best value for k.
#ii) Perform cross-validation to pick the best model between logistic regression and kNN. Does the answer change when you use different CV technique?


