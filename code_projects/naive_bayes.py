import pandas as pd
import random as rd
import string as st
import pprint as pp

import nltk.classify
from nltk import NaiveBayesClassifier


url_prefix = 'https://raw.github.com/dzorlu/GADS/master/data/nb_train.csv'
TRAIN_PCT = 0.7

TRAIN = '/Users/john/data/gads/nb_train.csv'
TEST = '/Users/john/data/gads/nb_test.csv'

#GIVEAWAYS = ['FAG', 'FAGGOT', 'FUCK', 'SLUT']

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
                all_insults.append(insult)

    # # shuffle all_names in place
    rd.shuffle(all_insults)
    
    return all_insults

def nltk_featurize(phrase):
    hfuck = 0
    if 'fuck' in phrase:
        hfuck = 1

    return {'has_fuck': hfuck }

    # """Returns ngrams and frequency distros """
    # phrase_tokens = {}

    # tokens = nltk.word_tokenize(phrase)
    # fd = nltk.FreqDist(tokens)

    # for token, cnt in fd.items():
    #     fdist = {}
    #     fdist['token']=token
    #     fdist['frequency']=cnt
    #     phrase_tokens['fdist'] = fdist

    # return phrase_tokens

    ### USE CODE BELOW FOR N-GRAMS ###

    # bgs = nltk.bigrams(tokens)
    # bg_fd = nltk.FreqDist(bgs)
    # for k,v in bg_fd.items():
    #     print k,v

def nltk_model(train_comments):
    for t in train_comments:
        print t 
    train_set = [(nltk_featurize(comment), is_insult) for comment, is_insult in train_comments]

    #train_set, test_set = features[:split_pt], features[split_pt:]
    nb = NaiveBayesClassifier.train(train_set)
        # labeled_featuresets - A list of classified
        # featuresets, i.e., a list of tuples (featureset, label).

    print nb.show_most_informative_features(2)

    print train_set

    # train_set = []
    # for t in train_comments:
    #     comment =  t['comment']
    #     features = nltk_featurize(comment) #this is creating a dict
    #     is_insult =  t['is_insult']
    #     tupl = (features, is_insult)
    #     #
    #     train_set.append(tupl)
    
if __name__ == '__main__':
	# train = process_data()
	# nltk_model()
    #bla = nltk_featurize('hello hello this is john bla bla bla')
    train = process_data()
    nltk_model (train)

# IDEAS -- > all caps
        #-- 
 
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