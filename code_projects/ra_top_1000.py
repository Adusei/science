from HTMLParser import HTMLParser
import urllib2

djs = []
# create a subclass and override the handler methods

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
	  print "Encountered a start tag:", tag
	def handle_endtag(self, tag):
	  print "Encountered an end tag :", tag
	def handle_data(self, data):
	  print "Encountered some data  :", data
	  djs.append(data)

def parse_top_1000(url):
	response = urllib2.urlopen(url)
	html = response.read()
	#print html

	start_str = ''
	end_str = '' 

	# instantiate the parser and fed it some HTML
	parser = MyHTMLParser()
	parser.feed(html)
	print str(djs)

if __name__ == '__main__':
	top_1000 = 'http://www.residentadvisor.net/dj.aspx'
	parse_top_1000(top_1000)