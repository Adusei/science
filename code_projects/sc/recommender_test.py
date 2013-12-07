import soundcloud as sc
import MySQLdb as mysql
import pprint as pp
import simple_regression as sr
import collections as cl
import operator as op


import nltk.classify
from nltk import NaiveBayesClassifier

user_ngram_fdist = cl.defaultdict(int)
my_favs = sr.get_my_favs()
# pp.pprint(my_favs)

for fav in my_favs:
	title =  fav['title']
	tag_list = fav['tags']
	# user_id = fav['user_id'] # Not sure how i want to do with this

	tag_list = tag_list.replace('"', '').lower()
	title = title.lower()

	title_tokens = nltk.word_tokenize(title)
	tag_tokens = nltk.word_tokenize(tag_list)

	tmp_tokens = title_tokens + tag_tokens

	bgs = nltk.bigrams(tmp_tokens)
	bg_fd = nltk.FreqDist(bgs)
	for ngram,freq in bg_fd.items():	
		ngram_str = ngram[0].encode('utf-8') + ' ' + ngram[1].encode('utf-8')
		user_ngram_fdist[ngram_str] += 1
		
sorted_ngrams = sorted(user_ngram_fdist.iteritems(), key=op.itemgetter(1))	
pp.pprint(sorted_ngrams)

	# def find_follower_likes

	# def classify_user
		# user = artist
		# user = listener


# the idea about a weighted graph
# in the way that "better" users
# titlt the graph in their favor
 


