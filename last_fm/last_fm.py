import urllib, urllib2
import pprint as pp
import simplejson as json
from last_db import DbTask
from last_db import StatementError




class LastFM(DbTask):
    def __init__(self):
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "834ca7240545d8fa587d43662c252773"
        # self.SECRET =  "44195d2012dd899f51af02c7861aad21" 

    # Define all of the methods that I inherit from DB task
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

    def get_relevant_tags_by_artist(self):
        return super(LastFM, self).get_relevant_tags_by_artist()

    def get_related_tags(self):
        return super(LastFM, self).get_related_tags()


    def api_request(self, **kwargs):
      json_response = {}

      ## Attribtues that are shared with all API requests
      kwargs.update({
          "api_key":  self.API_KEY,
          "format": "json",
          "limit": 1000
      })
      
      ## Encode the request into a
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

        self.set_tag_pct(artist_id, total_tag_count)


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

    def output_relevant_tags_by_artist(self):
        f = open('tags_for_artists.txt', 'w+')
        f.write('artist_name, tag_name, tag_count_pct\n')

        db_results = self.get_relevant_tags_by_artist()

        for r in db_results:
            f.write(r.artist_name + ',' + r.tag_name + ',' + str(r.tag_count_pct) + '\n')

        f.close()


    def output_related_tags(self):
        # get related tags from the database (see query in db method)
        db_results = self.get_related_tags()

        # Create a tuple-dict for DISTINCT results
        # this is more work, but the resulting data set is nicer

        distinct_results = {}
        for r in db_results:
            tpl = ( r.t1 , r.t2 ) 
            inv_tpl = ( r.t2 , r.t1 ) 

            try:
                # Only add the tag combo if id doesnt exist already
                distinct_results[inv_tpl]
            except KeyError:
                distinct_results[tpl] = r.score

        # Find the Max Score (to normalize btwn 0 and 1)
        # JD:  There has gotta be a better way to do this :-/ 
        max_key = max(distinct_results,key=distinct_results.get)
        max_value = distinct_results[max_key]

        # open the output file
        f = open('related_tags.txt', 'w+')

        #write the header
        f.write('tag_1, tag_2, score')

        # write each line sorted by 
        for tag_combo,score in sorted(distinct_results.items()):
            print tag_combo, score / max_value

            # ensure the score is between 0 and 1
            # FIX THISSSSSS!!! MAKE IT NORMAL  -- RESULTS WILL BE WAY NICER
            score_normal = ( score / max_value ) 
            # write the output to a file
            f.write(tag_combo[0] + ','  + tag_combo[1] + ',' +  str(score_normal) + '\n')

        f.close()



def main():
    last_task = LastFM()
    # last_task.get_artist_by_genre( "minimal techno" )
    last_task.output_relevant_tags_by_artist()
    # last_task.output_related_tags()
    
    
    # last_request.get_tags_by_artist("raresh")



if __name__ == "__main__": main()