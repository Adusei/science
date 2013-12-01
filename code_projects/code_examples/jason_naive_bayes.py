
import random
import string

import nltk.classify
from nltk import NaiveBayesClassifier

from sklearn import cross_validation as cv
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB

MALE_FILE = 'male.txt'
FEMALE_FILE = 'female.txt'

TRAIN_PCT = 0.7

def nltk_featurize(word):
    return {'last_two': word[-2:]}

def nltk_model():
    """Fits the (non-parametric) naive Bayes classifier from nltk on the names
    dataset."""
    # each elt of all_names will be a (name, gender) tuple
    all_names = list()

    with open(MALE_FILE, 'r') as f:
        for line in f:
            all_names.append((line.rstrip(), 'male'))   # rstrip removes trailing whitespace

    with open(FEMALE_FILE, 'r') as g:
        for line in g:
            all_names.append((line.rstrip(), 'female'))

    # assert stmts can be useful for debugging etc
    assert len(all_names) == 7944
    print type(all_names) 

    print '<-- this is the type for all names'
    for name in all_names:
        print type(name)


    # shuffle all_names in place
    random.shuffle(all_names)

    # features are ({'feature_type': feature_value}, gender) tuples
    features = [(nltk_featurize(name), gender) for name, gender in all_names]
    split_pt = int(TRAIN_PCT * len(features))

    train_set, test_set = features[:split_pt], features[split_pt:]
    nb = NaiveBayesClassifier.train(train_set)

    print 'accuracy = {0} %'.format(
        int(100 * nltk.classify.accuracy(nb, test_set)))
    nb.show_most_informative_features(10)

if __name__ == '__main__':
    # sklearn_model()
    nltk_model()

# read the docs!
# http://nltk.org/book/ch06.html