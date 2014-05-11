# last_db.py

from __future__ import absolute_import
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import StatementError
from sqlalchemy import desc

import sqlalchemy as al

import pprint as pp

class DbTask(object):

    # connect to local host
    db_connection_string  = 'mysql://root@localhost/last_fm'

    # create SQL Achemy 
    engine = create_engine(db_connection_string, convert_unicode=True,pool_recycle=3600, pool_size=20)

    # dont tell me everything thats going on with the database
    engine.echo = False

    # create session object
    db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))

    # define the metadata for my database ( need this to create table objects below )
    metadata = al.MetaData(engine)

    # create the sql alchemy table objects
    tags_table = al.Table('tags', metadata, autoload=True)
    artist_table = al.Table('artists', metadata, autoload=True)
    artist_to_tags_table = al.Table('artist_to_tags', metadata, autoload=True)

    def __init__(self):
        print("Initializing DBTask!")

    def add_artist (self, artist_name):
        # decode the artist name
        artist_name = artist_name.decode('utf8')
        try:
            # prepare insert statement
            artist_ins = self.artist_table.insert()

            #execute insert statement with provided param
            self.engine.execute(artist_ins,artist_name = artist_name)
            print 'success fully insertest tag: ' + artist_name

        # since there is a unique index on artist name the above code 
        # will only suceed when the artist_name does not exist in the artist table.
        except IntegrityError:
            pass

        # close the database connection
        self.db_session.close()


    def add_tag (self, tag_name):
        # decode the tag
        tag_name = tag_name.decode('utf8')
        try:
            #prepare the insert statement and execute with the provided tag name
            tag_ins = self.tags_table.insert()
            self.engine.execute(tag_ins,tag_name = tag_name)
            print '...success fully insertest tag ' + tag_name
        
        # only insert new tags... if tag exists above code will not run
        except IntegrityError:
            pass

        # close db connection
        self.db_session.close()

    def add_artist_to_tag (self, artist_id, tag_id, tag_count):
        try:
            # insert artist to tags based on provided params
            a_t_ins = self.artist_to_tags_table.insert()
            self.engine.execute(a_t_ins, artist_id = artist_id, tag_id = tag_id, tag_count = tag_count)

            # only exec above code if relation doesnt exists.. artist_id/tag_id is primary key.
        except IntegrityError:
            pass

        # close db connection
        self.db_session.close()

    def get_tag_by_name (self, tag_name):
        tag_name = tag_name.decode('utf8') 

        # select from the database where the tag name is what weve passed in
        where_clause = 'tag_name = "' + tag_name + '"'
        s = self.tags_table.select().where(where_clause)

        # execute the select and store row in rs
        rs = s.execute()

        # save the tag id and return it
        for r in rs:
            tag_id = r.tag_id

        self.db_session.close()
        return tag_id


    def get_artist_by_name(self, artist_name):
        artist_name = artist_name.decode('utf8') 

        where_clause = 'artist_name = "' + artist_name + '"'
        s = self.artist_table.select().where(where_clause) #.limit(1)
        # Since there is a unique index on artist_name dont need to limit

        rs = s.execute()

        for r in rs:
            artist_id = r.artist_id
            print artist_id
        
        self.db_session.close()
        return artist_id


    def set_tag_pct(self, artist_id, total_tag_count):
        # update the tag percentage to the tag count / the total tag count
        stmt = self.artist_to_tags_table.update().where(self.artist_to_tags_table.c.artist_id==artist_id).values(tag_count_pct = self.artist_to_tags_table.c.tag_count / total_tag_count )

        stmt.execute()


    def get_relevant_tags_by_artist(self):
        # select from DB the tags-artist relations and their names
        # for the sake of space... only show tags that represent at least 10 % of the whole
        raw_sql = '''
        SELECT  
            a.artist_name, t.tag_name, att.tag_count_pct  
        FROM artist_to_tags att
        INNER JOIN tags t
            ON att.tag_id = t.tag_id
        INNER JOIN artists a 
            ON att.artist_id = a.artist_id
        WHERE att.tag_count_pct > .1
        ORDER BY  artist_name
        '''

        # execute above statement and return results
        db_results =  self.engine.execute(raw_sql)
        return db_results

    def get_related_tags(self):
        #  dont just show me the number of times both tags show up together (count(*))
        #  show me the sum of all of the pct_counts for each time these appear...
        #  this means that if two tags that are very relevant to the artist appear x times together
        #  the score will be higher than if two tags appeared x times but were less relevant to that artist

        raw_sql = '''
        SELECT 
            t1.tag_name as t1, t2.tag_name as t2, x.score
        FROM
        (
            SELECT
                at_1.tag_id AS tag_id_1
                , at_2.tag_id AS tag_id_2
                #, count(*) as c
                , sum(at_1.tag_count_pct + at_2.tag_count_pct ) AS score
            FROM artist_to_tags at_1
                INNER JOIN artist_to_tags at_2
                ON at_1.artist_id = at_2.artist_id
                AND at_1.tag_id != at_2.tag_id
            GROUP BY at_1.tag_id, at_2.tag_id HAVING COUNT(*) > 10
        ) x
        INNER JOIN tags t1
            ON x.tag_id_1 = t1.tag_id
        INNER JOIN tags t2
            ON x.tag_id_2 = t2.tag_id
        ORDER BY x.score DESC
        '''

        # get the results of above query and return it
        db_results =  self.engine.execute(raw_sql)
        return db_results







