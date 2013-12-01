import pandas as pd
import random as rd
import string as st
import pprint as pp
from sklearn import cross_validation as cv


import nltk.classify
from nltk import NaiveBayesClassifier



url_prefix = 'https://raw.github.com/dzorlu/GADS/master/data/nb_train.csv'
NUM_FOLDS = 10

TRAIN = '/Users/john/data/gads/nb_train.csv'
TEST = '/Users/john/data/gads/nb_test.csv'


def process_data(): # FIX THIS!
    all_insults = list()

    with open(TRAIN, 'r') as f:
      for line in f:
        insult = {}
        arr = line.split(',')
        comment = arr[2]
        if comment.endswith('\n'): #FIX ASAP!!!!
            comment = comment.replace('"""','')
            comment = comment.strip()
            insult['comment'] = comment
            is_insult = arr[0]
            insult['is_insult'] = is_insult
            if len(comment) > 1:
                all_insults.append((comment,is_insult))
    
    return all_insults


def nltk_featurize(phrase):
    phrase_features = {}
    # hfag = 0

    # if 'fag' in phrase.lower():
    #     hfag = 1
     
    # phrase_features['has_fag'] = hfag

    ###          ###
    ##  TOKENIZE  ##
    ###          ###

    tokens = nltk.word_tokenize(phrase)
    fd = nltk.FreqDist(tokens)

    for token, cnt in fd.items():
        fdist = {}
        #phrase_features['word']=token
        phrase_features['']= (token,cnt)

    return phrase_features


    # {'has_fag': 0, 'has_fuck': 1, 'word': ('hello',2) }

    ### USE CODE BELOW FOR N-GRAMS ###

    # bgs = nltk.bigrams(tokens)
    # bg_fd = nltk.FreqDist(bgs)
    # for k,v in bg_fd.items():
    #     print k,v

# def nltk_model(train_comments):
def nltk_model(train_data, test_data, iteration):
    # assert len(train_comments) == 1000 #?

    test_set = [(nltk_featurize(comment), is_insult) for comment, is_insult in test_data]
    train_set = [(nltk_featurize(comment), is_insult) for comment, is_insult in train_data]    

    #train_set, test_set = features[:split_pt],features[split_pt:]
    
    nb = NaiveBayesClassifier.train(train_set)

        # labeled_featuresets - A list of
        # classified# featuresets, i.e., a 
        # list of tuples (featureset, label).

    nb.show_most_informative_features(10)
    
    print 'accuracy = {0} %'.format(int(100 * nltk.classify.accuracy(nb, test_set)))

def kfolds(features, labels,num_folds):
    kf = cv.KFold(n=len(features), n_folds=num_folds, shuffle=True)
    return kf

def cross_validate (data,excluded_feature=None):
# create cv iterator (note: train pct is set implicitly by number of folds)

    features = []
    labels = []

    for feature, label in data:
        features.append(feature)
        labels.append(label)

    num_recs = len(data)
    kf = kfolds(features, labels,NUM_FOLDS)

    for i, (train_index, test_index) in enumerate(kf):

        loop_ind = '\n'+ '=' * 20 + 'Loop Number: ' + str(i) + '=' * 20 

        print loop_ind * 3 + '\n'

        train_data = []
        test_data = []

        for t in train_index:
            ftr = features[t]
            lbl = labels[t]
            train_data.append((ftr,lbl))

        for t in test_index:
            ftr = features[t]
            lbl = labels[t]
            test_data.append((ftr,lbl))
            
        nltk_model(train_data, test_data, i)

if __name__ == '__main__':
	# train = process_data()
	# nltk_model()
    #bla = nltk_featurize('hello hello this is john bla bla bla')
    train = process_data()
    # nltk_model (train)
    cross_validate (train)

## IDEAS ## 

## all caps
## ngrams

## HOMEWORK ASSIGNMENT ##
 
# The challenge is to detect when a comment from a conversation 
# would be considered insulting to another participant in the 
# conversation. The data consists of a label column followed 
# by two attribute fields.

# This is a single-class classification problem. The label
# is either 0 meaning a neutral comment, or 1 meaning an 
# insulting comment (neutral can be considered as not belonging
# to the insult class. Your predictions must be an integer.

# The first attribute is the time at which the comment was made. 
# It is sometimes blank, meaning an accurate timestamp is not 
# possible. It is in the form "YYYYMMDDhhmmss" and then the Z 
# character. It is on a 24 hour clock and corresponds to the 
# localtime at which the comment was originally made.

# The second attribute is the unicode-escaped text of the 
# content, surrounded by double-quotes. The content is mostly
# english language comments, with some occasional formatting.

# Please submit your predictions -0 or 1- in a csv format.
# Make sure that your submission has exactly 2000 entries.