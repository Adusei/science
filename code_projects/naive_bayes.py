import pandas as pd
import random as rd
import string as st
from collections import Counter


import nltk.classify
from nltk import NaiveBayesClassifier

from sklearn import cross_validation as cv
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB

url_prefix = 'https://raw.github.com/dzorlu/GADS/master/data/'
TRAIN_PCT = 0.7

def process_data():
	train_location = 'nb_train.csv'
	test_location =  'nb_test.csv'

	train_url = url_prefix + train_location
	test_url  = url_prefix + test_location

	train_data = pd.read_csv(train_url)
	test_data = pd.read_csv(test_url)

	return train_data

def nltk_featurize(comments):
	lines = comments.drop('insult',1)
	#lines = lines.drop('date',1)
	
	print '^ comments ^'
	lines = comments

	for line in lines:
		counts = Counter(line)
		print counts
		print line

		#Counter({'this': 1, 'a': 1, 'is': 1, 'sentence': 1})

    # underfitting! can do somewhat better
    # return {'last_letter': word[-1]}

    # overfitting! features have little traction
    # return dict(('contains_' + k, k in word.lower()) for k in string.lowercase)


if __name__ == '__main__':
	train = process_data()
	nltk_featurize(train)

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