from HTMLParser import HTMLParser

import urllib2

djs = []

class MyHTMLParser(HTMLParser):
    def add_dj(self, html):
        self.attr_list = []
        self.dj = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.attr_list.append(attrs)
        
    def handle_endtag(self, tag):
        self.attr_list.pop()
        t = tag
    def handle_data(self, data):
        #if len(attr_list) > 0:
        for k,v in self.attr_list:
            k == 'href' and v.startswith('/dj/'):
                print 'dj: ' + str(v)
                self.dj['permalink'] = v
                self.dj['name'] = data
                djs.append(self.dj)

    
response = urllib2.urlopen('http://www.residentadvisor.net/dj.aspx?style=15&1000=1')
html = response.read()

p = MyHTMLParser()
p.add_dj(html)
print '--- DJS -->' + str(djs) + '<-- DJS ---'

#http://stackoverflow.com/questions/7204056/python-htmlparser
#print str(djs)

# <a href="/dj/donkanalie">Don Kanalie</a>
# <br /><a href="/dj/donramon">Don Ramon</a><br />

