from HTMLParser import HTMLParser
import urllib2

##http://www.residentadvisor.net/dj.aspx?style=20 #deephouse
##http://www.residentadvisor.net/dj.aspx?style=5 #tech


#def get_genres(self):
	## look at the drop down menu in the source here:view-source:http://www.residentadvisor.net/dj.aspx#A

def bla():
	genre_iterator = [{'DeepHouse':20}
	,{'Techno':5}
	,{'Tech House':15}]

	for x in genre_iterator:
		for k,v in x.items():
			print 'key: '  + str(k) + ' val: '  + str(v)
		#print 'value' + v

# create a subclass and override the handler methods

'''
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
'''
if __name__ == '__main__':
	#top_1000 = 'http://www.residentadvisor.net/dj.aspx'
	bla()