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
from sklearn.linear_model import LogisticRegression as LR


data_url = 'https://raw.github.com/dzorlu/GADS/4c3ee79773d3c6024979e20d337ad2210be68ac9/data/wine.txt'

NUM_NBRS = 21
FOLDS = 20
RESULTS = []
CROSS_VAL_ARRAY = []
LOG_REG_ARRAY = []
VIZ_ARRAY = []

def process_data(data_src):
  header = ['label','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
  data = pd.read_csv(data_src,header=None,names=header)

  features = data.drop('label', 1)
  labels = data.label 

  #run_knn(features, labels, features,labels,1,5)
  run_log_reg(features, labels)
  #cross_val( features, labels, FOLDS ,NUM_NBRS)
  #find_opt_k ( features, labels )

def cross_val(features, labels, num_folds, k=None, algo='knn'):
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
    cv_results['algo'] = algo
    RESULTS.append(cv_results)
    VIZ_ARRAY.append(1 - avg_acc)
    print cv_results

def find_opt_k(features,labels):
    CROSS_VAL_ARRAY = []
    nmbs =list(range(1,51))
    for nm in nmbs:
      if nm % 2 != 0:
        loop_ind = '\n'+ '=' * 20 + 'k: ' + str(nm) + '=' * 20 
        print loop_ind * 3 + '\n'
        cross_val (features, labels, FOLDS, nm,'knn')

def run_knn(train_features, train_labels,test_features, test_labels, iteration=None,k=None):
    clf = knn(n_neighbors = k)
    clf.fit(train_features, train_labels)

    acc = clf.score(test_features, test_labels)

    predicted_labels = clf.predict(test_features)
    cm = confusion_matrix(test_labels, predicted_labels)

    CROSS_VAL_ARRAY.append(acc)

def kfolds(features, labels,num_folds):
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True)
    return kf

def run_log_reg (features, labels):
    #model_results = {}
    #num_recs = len(data)
    kf = kfolds(features, labels, FOLDS)

    for i, (train_index, test_index) in enumerate(kf):
      model = LR()

      train_features = features.loc[train_index].dropna()
      train_labels = labels.loc[train_index].dropna()

      test_features = features.loc[test_index].dropna()
      test_labels = labels.loc[test_index].dropna()

      model.fit(train_features, train_labels)
      # get model outputs
      inputs = map(str, train_features.columns.format())
      coeffs = model.coef_[0]
      accuracy = model.score(test_features, test_labels)

      print 'accuracy:' + str(accuracy)

if __name__ == '__main__':
  process_data(data_url)
  pp.pprint(RESULTS)
  #print '\n\n'
  #print VIZ_ARRAY

#http://archive.ics.uci.edu/ml/datasets/Wine
#i) Fit a kNN algorithm. Perform cross-validation to pick the best value for k.
    # -> k = 9 
    # how do i balance a high accuracy for a low 
    # value of k given that when k approaches zero
    # the model becomes over fit?

#ii) Perform cross-validation to pick the best model between logistic regression and kNN. Does the answer change when you use different CV technique?


# TODO - > Find Variance
# CV on Features
# move all code to m_learning Repo

