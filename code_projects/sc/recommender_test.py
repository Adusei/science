import soundcloud as sc
import MySQLdb as mysql
import pprint as pp
import simple_regression as sr

import nltk.classify
from nltk import NaiveBayesClassifier

user_ngram_fdist = {}
my_favs = sr.get_my_favs()
# pp.pprint(my_favs)

for fav in my_favs:
	title =  fav['title']
	tag_list = fav['tags']
	user_id = fav['user_id']
	print user_id

	tag_list = tag_list.replace('"', '').lower()
	title = title.lower()

	# print 'tag list: ' + tag_list.lower()
	# print 'title: ' + title.lower()
	title_tokens = nltk.word_tokenize(title)
	tag_tokens = nltk.word_tokenize(tag_list)

	tmp_tokens = title_tokens + tag_tokens

	bgs = nltk.bigrams(tmp_tokens)
	bg_fd = nltk.FreqDist(bgs)
	for ngram,freq in bg_fd.items():
	 	print ngram, freq
	 	# Add to user_ngram_fdist hash ..
	 	print '^^^ TAG TOKENS ^^^'
		
	



