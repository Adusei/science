import urllib, urllib2
import pprint as pp
import simplejson as json
from last_db import DbTask
from last_db import StatementError


# SOURCE: http://snipplr.com/view/63161/

class LastFM(DbTask):
    def __init__(self):
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "834ca7240545d8fa587d43662c252773"
        # self.SECRET =  "44195d2012dd899f51af02c7861aad21" 

    def add_artist(self,artist_name):
        super(LastFM, self).add_artist(artist_name)

    def add_tag(self,tag_name):
        super(LastFM, self).add_tag(tag_name)

    def add_artist_to_tag(self,artist_id,tag_id,tag_count):
        super(LastFM, self).add_artist_to_tag(artist_id,tag_id,tag_count)

    def select_artists(self):
        return super(LastFM, self).select_artists()

    def get_artist_by_name(self, artist_name):
        return super(LastFM, self).get_artist_by_name(artist_name)

    def get_tag_by_name(self, tag_name):
        return super(LastFM, self).get_tag_by_name(tag_name)

    def set_tag_pct(self, artist_id, total_tag_count):
        super(LastFM, self).set_tag_pct(artist_id,total_tag_count)

    # artist_id = self.get_artist_by_name(artist_name) 
    # tag_id = self.get_tag_by_name(tag_name)

    default = False

    def api_request(self, **kwargs):
      json_response = {}
      kwargs.update({
          "api_key":  self.API_KEY,
          "format": "json",
          "limit": 3
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

    def get_tags_by_artist (self, artist_name, **kwargs):
        kwargs.update({
            "method": "artist.gettoptags",
            "artist":   artist_name,
        })

        response_data = self.api_request(**kwargs)

        tags = response_data['toptags']['tag']
        
        total_tag_count = 0

        for tag in tags:
            tag_name = tag['name'].encode('utf8')
            tag_count = tag['count']
            total_tag_count = total_tag_count + int(tag_count)

            try:
                self.add_tag(tag_name)

                artist_id = self.get_artist_by_name(artist_name) 
                tag_id = self.get_tag_by_name(tag_name)

                self.add_artist_to_tag(artist_id, tag_id, tag_count)

                print tag_name
            except StatementError:
                pass

        # try:
        self.set_tag_pct(artist_id, total_tag_count)
        # except :


    def get_artist_by_genre(self, genre, **kwargs):
        kwargs.update({
            "method": "tag.gettopartists",
            "tag":    genre,
        })

        response_data = self.api_request(**kwargs)

        artists =  response_data['topartists']['artist']
        for artist in artists:
            artist_name =  artist['name'].encode('utf8')
            self.add_artist(artist_name)
            print artist_name + '\n' +'=' * 50
            self.get_tags_by_artist(artist_name)

  

def main():
    last_request = LastFM()
    last_request.get_artist_by_genre( "minimal techno" )
    # last_request.get_tags_by_artist("raresh")



if __name__ == "__main__": main()