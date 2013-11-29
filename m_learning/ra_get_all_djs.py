from HTMLParser import HTMLParser

import urllib2
import pprint as pp
import json

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
            DJS.append(self.dj)


response = urllib2.urlopen('http://www.residentadvisor.net/dj.aspx?style=15&1000=1')
html = response.read()

p = MyHTMLParser()
p.add_dj(html)

pp.pprint(DJS)


#http://stackoverflow.com/questions/7204056/python-htmlparser
#print str(djs)

# <a href="/dj/donkanalie">Don Kanalie</a>
# <br /><a href="/dj/donramon">Don Ramon</a><br />

# ['/dj/leecurtiss']
# ['/dj/livioroby']
# ['/dj/livioroby', 'Livio ', '/dj/losoul']
# ['/dj/livioroby', 'Livio ', '/dj/lucabacchetti']
# ['/dj/livioroby', 'Livio ', '/dj/lukesolomon']
# ['/dj/livioroby', 'Livio ', '/dj/lunacityexpress']
# ['/dj/monikakruse']

