import numpy as np
import pandas as pd
import urllib2 as ul

from sklearn.linear_model import LogisticRegression as LR
from sklearn.metrics import confusion_matrix

INPUT_FILE = 'beer.txt'
TRAIN_PCT = 0.7

def preprocess_data(input_file=INPUT_FILE):
    beer = pd.read_csv(input_file, delimiter='\t').dropna()
    
    # add column for class labels (1 for top half, 0 for bottom half)
    midpt = int(len(beer) / 2)
    beer['label'] = beer['Rank'].map(lambda k: 1 if k <= midpt else 0)
    # (buzzwords: map, anonymous function, ternary operator...look these up!)

    return beer[['ABV', 'Reviews', 'label']]

def run_model(data):
    """Perform train/test split, fit model and output results."""

    # shuffle dataset
    data = data.reindex(np.random.permutation(data.index))

    split_pt = int(TRAIN_PCT * len(data))

    print '=' * 100
    print ' ' * 20  + '.... the data set has ' +  str(len(data)) + ' total records and the md mpt is ' + str(split_pt) + '....'
    print '=' * 100

    train_x = data[:split_pt].drop('label', 1)      # training set features
    train_y = data[:split_pt].label                 # training set target

    '''
    print train_x
    print train_x.values 
    print '=' * 100
    print '=' * 100
    print train_y.values
    print train_y
    '''
    
    test_x = data[split_pt:].drop('label', 1)       # test set features
    test_y = data[split_pt:].label                  # test set target

    # initialize model & perform fit
    model = LR()                        # model is an "instance" of the class LR
    model.fit(train_x, train_y)         # perform model fit ("in place")

    print model
    
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
    beer = preprocess_data()
    # beer = preprocess_data()
    run_model(beer)


# CHALLENGE QUESTIONS!
# 1) what do the accuracy results suggest?
# 2) how do your results change if you try to predict the top 10%
#    instead of the top half? what does this suggest?
# 3) if you run this several times, your results may vary widely. how could you
#    stabilize this behavior?
# 4) why should you worry about a train/test split?
# 5) the model object has attributes called "model.penalty" and "model.c". What
#    are these values used for?

#notes
 #minimize your generalization error (dont memorize the practice problems...)
 #try test fitting => prevents overfitting
 #shuffling => prevents bais
 
##################
### QUESTIONS ####
##################

#response = ul.urlopen('https://raw.github.com/dzorlu/GADS/master/data/beer.txt')
#INPUT_FILE = response.read()#'beer.txt'

    ## IF I HAVE WANT TO PUT A RESPONSE LIKE 
    ## I HAVE ABOVE INTO PANDAS HOW DO I DO SO?
