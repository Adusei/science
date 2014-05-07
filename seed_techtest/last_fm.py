import urllib, urllib2
import pprint as pp
import simplejson as json
 
# SOURCE: http://snipplr.com/view/63161/

class LastFM:
    def __init__(self ):
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "834ca7240545d8fa587d43662c252773"
        # self.SECRET =  "44195d2012dd899f51af02c7861aad21" 

    def api_request(self, url):
				#Send Request and Collect it
				data = urllib2.urlopen( url )
				json_response = json.load ( data )

				data.close()
				return json_response


    # def get_tags_by_artist (self, artist):
    # 		url = "http://ws.audioscrobbler.com/2.0/?method=artist.getTags&artist=Red%20Hot%20Chili%20Peppers&user=RJ&api_key=834ca7240545d8fa587d43662c252773&format=json"

    def get_genre(self, genre, **kwargs):
        kwargs.update({
            "method":	"tag.gettopartists",
            "tag":		genre,
            "api_key":	self.API_KEY,
            "limit":	100,
            "format":	"json"
        })
        try:
						#Create an API Request
						url = self.API_URL + "?" + urllib.urlencode(kwargs)

						response_data = self.api_request(url)

						artists =  response_data['topartists']['artist']
						for artist in artists:
						    print artist['name'].encode('utf8')
						#Close connection
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
 
def main():
    last_request = LastFM()
    last_request.get_genre( "minimal" )
 
if __name__ == "__main__": main()