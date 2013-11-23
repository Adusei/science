from HTMLParser import HTMLParser
import urllib2
import sys

OUTPUT_FILE = '/Users/john/data/ra_raw/TECHNO.html'

f = open(OUTPUT_FILE, 'w')
djs = []
#genre_iterator = [{'DeepHouse':20}
#,{'Techno':5}
#,{'Tech House':15}]

genre_iterator  = [{'Techno':5}]

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		a = 1
	def handle_endtag(self, tag):
	  b = 2
	def handle_data(self, data):
	  print "Encountered some data  :", data
	  djs.append(data)

def get_raw_html(url):
	response = urllib2.urlopen(url)
	html = response.read()
	f.write(html)

def save_raw_files():
	for x in genre_iterator:
		for genre,genre_id in x.items():
			print 'genre: '  + str(genre) + ' genre_id: '  + str(genre_id)
			request_str = 'http://www.residentadvisor.net/dj.aspx?style=' + str(genre_id)
			get_raw_html(request_str)
			#return raw_html
			#genre_source_html = get_html(raw_html)

def parse_html(html):
	parser = MyHTMLParser()
	parser.feed(html)

if __name__ == '__main__':
	# rw = save_raw_files()
	f = open(OUTPUT_FILE, 'r')
	print f
	html = f.readlines()
	for line in html:
			print line
			
	#parse_html(html)
	#print djs

	#f.write(rw)
	#print djs

