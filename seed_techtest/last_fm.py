import urllib, urllib2
import pprint as pp
import simplejson as json
 
# SOURCE: http://snipplr.com/view/63161/

class LastFM:
    def __init__(self ):
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "834ca7240545d8fa587d43662c252773"
        # self.SECRET =  "44195d2012dd899f51af02c7861aad21" 

    def api_request(self, **kwargs):
      json_response = {}
      kwargs.update({
          "api_key":  self.API_KEY,
          "format": "json"
      })

      url = self.API_URL + "?" + urllib.urlencode(kwargs)
      
      try:
          # Send Request and Collect it
          data = urllib2.urlopen( url )
          json_response = json.load ( data )

          data.close()

      except urllib2.HTTPError, e:
          print "HTTP error: %d" % e.code
      except urllib2.URLError, e:
          print "Network error: %s" % e.reason.args[1]

      return json_response

    def get_tags_by_artist (self, artist, **kwargs):
        kwargs.update({
            "method": "artist.gettoptags",
            "artist":   artist,
        })

        response_data = self.api_request(**kwargs)

        tags = response_data['toptags']['tag']
        for tag in tags:
            print tag['name'].encode('utf8')

    def get_artist_by_genre(self, genre, **kwargs):
        kwargs.update({
            "method": "tag.gettopartists",
            "tag":    genre,
            "limit":  10,
        })

        response_data = self.api_request(**kwargs)

        artists =  response_data['topartists']['artist']
        for artist in artists:
            artist_name =  artist['name'].encode('utf8')
            print artist_name + '\n' +'=' * 50
            self.get_tags_by_artist(artist_name)

 
def main():
    last_request = LastFM()
    # last_request.get_tags_by_artist( "raresh" )
    last_request.get_artist_by_genre( "minimal techno" )
 
if __name__ == "__main__": main()