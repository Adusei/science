import urllib, urllib2
import pprint as pp
import simplejson as json
from db import DbTask
from db import StatementError
import numpy as np


class LastFM(DbTask):
    def __init__(self):
        # define my api credentials
        self.API_URL = "http://ws.audioscrobbler.com/2.0/"
        self.API_KEY = "834ca7240545d8fa587d43662c252773"
        # self.SECRET =  "44195d2012dd899f51af02c7861aad21" 

    ## Define all of the methods that I inherit from DB task ##
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

      ## update the request obect with attribtues 
      ## that are shared with all API requests
      kwargs.update({
          "api_key":  self.API_KEY,
          "format": "json",
          "limit": 1000
      })
      
      ## Encode the request into a URL
      url = self.API_URL + "?" + urllib.urlencode(kwargs)

      
      try:
          # Send Request and Collect it
          data = urllib2.urlopen( url )
          # decode json
          json_response = json.load ( data )

          data.close()

      # provive URL and HTTP exceptions for API requests
      except urllib2.HTTPError, e:
          print "HTTP error: %d" % e.code
      except urllib2.URLError, e:
          print "Network error: %s" % e.reason.args[1]

      return json_response


    def get_artist_by_genre(self, genre, **kwargs):
        # prepare the request object with the genre and the api method
        kwargs.update({
            "method": "tag.gettopartists",
            "tag":    genre,
        })

        # send request to api and store the response
        response_data = self.api_request(**kwargs)

        # access the artists dictionary from the response
        artists =  response_data['topartists']['artist']
        for artist in artists:

            # encode the artist name
            artist_name =  artist['name'].encode('utf8')

            # add this artists into the database (see db.py)
            self.add_artist(artist_name)

            # print out the artist name for debugging  
            print artist_name + '\n' +'=' * 50

            # find relevant tags for the artist and save those to the DB as well
            self.get_tags_by_artist(artist_name)

    def get_tags_by_artist (self, artist_name, **kwargs):
        # set the additioal parameters for this particulare API request
        kwargs.update({
            "method": "artist.gettoptags",
            "artist":   artist_name,
        })

        # get data from api using the api_request method (above)
        response_data = self.api_request(**kwargs)

        # access just the tags data from the response
        tags = response_data['toptags']['tag']
        
        # prepare to find the total count of tags for each artist in order to
        # determine the relevance each tag is to the artist
        total_tag_count = 0

        for tag in tags:
            # get the encoded tag name and tag count for each result
            tag_name = tag['name'].encode('utf8')
            tag_count = tag['count']

            # for each iterationn, add the tag count to the total (  )
            total_tag_count = total_tag_count + int(tag_count)

            try:
                # add the tag to the DB
                self.add_tag(tag_name)

                # find the artist and tag id (see db.py)

                artist_id = self.get_artist_by_name(artist_name) 
                tag_id = self.get_tag_by_name(tag_name)

                # add the artist_id, tag_id relation and the tag count (see db.yp)
                self.add_artist_to_tag(artist_id, tag_id, tag_count)

                print tag_name # for debugging

            # this try/except block deals with the issue in which a tag is BLANK
            # i consider this bad data, but regardless this issue had to be dealt with
            except StatementError:
                pass

        # update the tag percentage column for each tag
        self.set_tag_pct(artist_id, total_tag_count)


    def output_relevant_tags_by_artist(self):
        # open the output file
        f = open('tags_for_artists.txt', 'w+')

        # write the header
        f.write('artist_name, tag_name, tag_count_pct\n')

        # get tags by artists from the databbase
        db_results = self.get_relevant_tags_by_artist()

        for r in db_results:

            # for each result add the artist and the tag to the output file
            f.write(r.artist_name + ',' + r.tag_name + ',' + str(r.tag_count_pct) + '\n')

        # close the file
        f.close()


    def output_related_tags(self):
        # get related tags from the database ( see query in db.py )
        db_results = self.get_related_tags()

        # create a tuple dictionary to store the tag combo, and the score
        # this data structure enables us to perform simple statistic analysis on the results
        tuple_dict_result = {}
        for r in db_results:

            # Create a tuple for each tag pair
            tpl = ( r.t1 , r.t2 ) 

            # assign the score to that tuple in the dictionary
            tuple_dict_result[tpl] = r.score


        # open the output file
        f = open('related_tags.txt', 'w+')

        #write the header
        f.write('tag_1, tag_2, score')

        # Calculate the standard deviation and the average of the data set
        score_stdv = np.std(tuple_dict_result.values())
        score_avg = np.average(tuple_dict_result.values())

        # iterate through the tags in alphabetical order
        for tag_combo,score in sorted(tuple_dict_result.items()):

            # calculate the z-score for the distribution
            zscore =  ( score - score_avg )  / score_stdv

            # write the output to a file
            f.write(tag_combo[0] + ','  + tag_combo[1] + ',' +  str(zscore) + '\n')

        #close the file
        f.close()



def main():
    ### INSTANTIATE THE LASTFM OBJECT ###
    last_task = LastFM()

    ### RUN TOP LEVEL METHOD - GET ALL ARTISTS AND THEN GET THEIR TAGS ###
    ### THIS POPULATES TRANSITIONAL DATASET
    last_task.get_artist_by_genre( "minimal techno" )

    ### OUTPUT THE TRANSITIONAL DATA SET ###
    last_task.output_relevant_tags_by_artist()

    ### OUTPUT THE FINAL RESULTS ###
    last_task.output_related_tags()
    

if __name__ == "__main__": main()