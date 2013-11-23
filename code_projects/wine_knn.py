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

NUM_NBRS = 5
MESH_SIZE = 0.02

COLORS_1 = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
COLORS_2 = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

def process_data(data_src):
	header = ['label','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','OD280/OD315 of diluted wines','Proline']
	data = pd.read_csv(data_src,header=None,names=header)

	features = data.drop('label', 1)
	labels = data.label 

	run_knn( features, labels,features, labels )

def run_knn(train_features, train_labels,test_features, test_labels):

    clf = knn(n_neighbors = NUM_NBRS)
    clf.fit(train_features, train_labels)

    # get accuracy (predictions made internally)
    acc = clf.score(test_features, test_labels)

    # get conf matrix (requires predicted labels)
    predicted_labels = clf.predict(test_features)
    cm = confusion_matrix(test_labels, predicted_labels)

    print 'k = {0}'.format(NUM_NBRS)
    #print 'num_features = {0}'.format(num_features)
    print 'accuracy = {0} %\n'.format(round(100 * acc, 2))
    print 'confusion matrix:\n', cm, '\n'


#def kfolds: 
	#print 'foo'

#def nested_cv:
	#print 'bar'


if __name__ == '__main__':
	process_data(data_url)


#http://archive.ics.uci.edu/ml/datasets/Wine
#i) Fit a kNN algorithm. Perform cross-validation to pick the best value for k.
#ii) Perform cross-validation to pick the best model between logistic regression and kNN. Does the answer change when you use different CV technique?


