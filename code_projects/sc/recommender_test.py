import soundcloud as sc
import MySQLdb as mysql
import pprint as pp
import simple_regression as sr

import nltk.classify
from nltk import NaiveBayesClassifier

phrase_features = {}

my_favs = sr.get_my_favs()
# pp.pprint(my_favs)

tokens = []

for fav in my_favs:
	title =  fav['title']
	tag_list = fav['tags']

	tmp_tokens = nltk.word_tokenize(title)
	# for tag in tag_list:
	# 	tmp_tokens.append(nltk.word_tokenize(tag))

	bgs = nltk.bigrams(tmp_tokens)
	bg_fd = nltk.FreqDist(bgs)
	for ngram,freq in bg_fd.items():
	 	print ngram, freq
		phrase_features['ngram']= (ngram,freq)


fd = nltk.FreqDist(tokens)
print type(fd)

	



