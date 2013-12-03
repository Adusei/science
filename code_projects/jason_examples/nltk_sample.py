import nltk
import pandas as pd
import random
import string

from nltk import NaiveBayesClassifier

import nlkt.classify



sentence = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)
print tokens

male_data = 'male.txt'
female_data = 'female.txt'

'''
m = 'https://raw.github.com/dzorlu/GADS/master/data/male.txt'
f = 'https://raw.github.com/dzorlu/GADS/master/data/female.txt'

male_data = pd.read_csv(m,header=None)
female_data = pd.read_csv(f,header=None)
'''

print 'male:' + str(male_data)
print 'femmale:' + str(female_data)

def nltk_featurize(word):
	return{'last_letter': word[-1]}
	return{'ae_in': 'ae' in word.lower()}

def nltk_model():
	for line in male_data: 
		all_names =	append((lien.rstrip(),'male'))

	for line in female_data: 
		all_names =	append((lien.rstrip(),'female'))

	asset len(all_names) == 7944

	random.shuffle(all_names) #changes in places....dos not create another varable

	features = [nltk_featurize(all_names), gender)
		for name, gender in all_names]

def sklearn_model(): #parametric.. using gausian distribution for feature  - > non parametric.. BIN then... bucket them
	iris = load_iris()
	tts = cv.train_test_split(iris.data, iris.target, train_size = .7)

	## Gausian assuption is Strong and Accurate

if __name__ = "__main__"




# Most Informative Features --> Value of likelyhood function
# pandas for line in line... use map (applies function to every column)

# read the docs!
# http://nltk.org/book/ch06.html

# Check out /.jq parser

# Andrew Ng
# http://cs229.stanford.edu/