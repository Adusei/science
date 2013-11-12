import numpy as np 
import pandas as pd

from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import confusion_matrix

#want to predict if my beer comes up in the top half

INPUT_FILE = '/data/beer.txt'
TRAIN_PCT = 0.7

  midpt = int(len(beer) / 2)
  beer['label'] = beer['Rank'].map(lambda k: 1 if k <= midpt else 0) #turnary operator
  	#map means to apply function to every item in the list


def run_model(data):
    """Perform train/test split, fit model and output results."""

    # shuffle dataset
    data = data.reindex(np.random.permutation(data.index))

    # perform train/test split (more about this next lecture!)
    split_pt = int(TRAIN_PCT * len(data))

    train_x = data[:split_pt].drop('label', 1)      # training set features
    train_y = data[:split_pt].label                 # training set target
    #index slicing

    test_x = data[split_pt:].drop('label', 1)       # test set features
    	#without label colum
    test_y = data[split_pt:].label                  # test set target
    	#with only label column
    	#splitting this into xs and ys

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




if __name__ == '__main__':
    beer = preprocess_data(simple=1)
    # beer = preprocess_data()
    run_model(beer)



#notes
 #minimize your generalization error (dont memorize the practice problems...)

 #try test fitting => prevents overfitting
 #shuffling => prevents bais
 




