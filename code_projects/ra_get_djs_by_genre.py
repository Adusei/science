from HTMLParser import HTMLParser
import urllib2
import sys

djs = []
genre_iterator = [{'DeepHouse':20}
,{'Techno':5}
,{'Tech House':15}]

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		a = 1
	def handle_endtag(self, tag):
	  b = 2
	def handle_data(self, data):
	  print "Encountered some data  :", data
	  djs.append(data)

def get_html(url):
	response = urllib2.urlopen(url)
	html = response.read()
	parser = MyHTMLParser()
	parser.feed(html)

def get_artists():
	for x in genre_iterator:
		for genre,genre_id in x.items():
			print 'genre: '  + str(genre) + ' genre_id: '  + str(genre_id)
			request = 'http://www.residentadvisor.net/dj.aspx?style=' + str(genre_id)
			genre_source_html = get_html(request)

if __name__ == '__main__':
	get_artists()
	print djs

