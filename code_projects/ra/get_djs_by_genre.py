from HTMLParser import HTMLParser
import urllib2
import sys
import pprint as pp

#genre_iterator  = [{'Techno':5}] # [{'DeepHouse':20},{'Tech House':15}]

DJS = []

class MyHTMLParser(HTMLParser):
    def add_dj(self, html):
        self.dj = {}
        self.attr_list = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.dj = {}
        self.attr_list = []
        for k,v in attrs:
            if k == 'href' and v.startswith('/dj/'):
                self.attr_list.append(v)

    def handle_endtag(self, tag):
        if len(self.attr_list) > 0:
            self.dj['permalink'] = self.attr_list[0]
            self.attr_list.pop()

    def handle_data(self, data):
       if len(self.attr_list) == 1:
            self.dj['name']= data
            try:
                self.dj[data]
            except ValueError:
                print 'does not exists already.. adding now'
            DJS.append(self.dj)
	
def get_raw_html(url):
	response = urllib2.urlopen(url)
	html = response.read()


def parse_html(html):
	p = MyHTMLParser()
	p.add_dj(html)

if __name__ == '__main__':
    response = urllib2.urlopen('http://www.residentadvisor.net/dj.aspx?style=15&1000=1')
    html = response.read()
    p = MyHTMLParser()
    p.add_dj(html)

    pp.pprint(DJS)


# try an assertion... should be 1000 items in dict


