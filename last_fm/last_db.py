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
    # ensures the connection the the database is closed on task completion
    db_connection_string  = 'mysql://root@localhost/last_fm'

    engine = create_engine(db_connection_string, convert_unicode=True,pool_recycle=3600, pool_size=20)
    engine.echo = False
    db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))

    metadata = al.MetaData(engine)

    def __init__(self):
        print("Initializing DBTask!")

    def add_artist (self, artist_name):
        artist_table = al.Table('artists', self.metadata, autoload=True)
        artist_name = artist_name.decode('utf8')
        try:
            artist_ins = artist_table.insert()
            self.engine.execute(artist_ins,artist_name = artist_name)
            print '...success fully insertest tag!!' + artist_name
        except IntegrityError:
            pass

        self.db_session.close()
        # http://stackoverflow.com/questions/8585346/get-last-inserted-value-from-mysql-using-sqlalchemy    
        ## DO THIS BEFORE HANDING IN THE CODE... WHAT IS BELOW IS GARBAGE ##

    def add_tag (self, tag_name):
        tags_table = al.Table('tags', self.metadata, autoload=True)
        tag_name = tag_name.decode('utf8')
        try:
            tag_ins = tags_table.insert()
            self.engine.execute(tag_ins,tag_name = tag_name)
            print '...success fully insertest tag ' + tag_name
        except IntegrityError:
            pass

        self.db_session.close()

    def add_artist_to_tag (self, artist_id, tag_id, tag_count):
        artist_to_tags_table = al.Table('artist_to_tags', self.metadata, autoload=True)

        try:
            a_t_ins = artist_to_tags_table.insert()
            self.engine.execute(a_t_ins, artist_id = artist_id, tag_id = tag_id, tag_count = tag_count)
        except IntegrityError:
            pass

        self.db_session.close()


    def get_tag_by_name (self, tag_name):
        tags_table = al.Table('tags', self.metadata, autoload=True)
        tag_name = tag_name.decode('utf8') 

        where_clause = 'tag_name = "' + tag_name + '"'
        s = tags_table.select().where(where_clause)

        rs = s.execute()

        for r in rs:
            tag_id = r.tag_id
            print tag_id

        self.db_session.close()
        return tag_id


    def get_artist_by_name(self, artist_name):
        artist_table = al.Table('artists', self.metadata, autoload=True)
        artist_name = artist_name.decode('utf8') 


        where_clause = 'artist_name = "' + artist_name + '"'
        s = artist_table.select().where(where_clause) #.limit(1)
        # Since there is a unique index on artist_name dont need to limit

        rs = s.execute()

        for r in rs:
            artist_id = r.artist_id
            print artist_id
        
        self.db_session.close()
        return artist_id


    def set_tag_pct(self, artist_id, total_tag_count):
        artist_to_tags_table = al.Table('artist_to_tags', self.metadata, autoload=True)
        stmt = artist_to_tags_table.update().where(artist_to_tags_table.c.artist_id==artist_id).values(tag_count_pct = artist_to_tags_table.c.tag_count / total_tag_count )

        stmt.execute()


    def output_relevant_tags_by_artist(self):
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

        db_results =  self.engine.execute(raw_sql)

        f = open('tags_for_artists.txt', 'w+')
        f.write('artist_name, tag_name, tag_count_pct\n')

        for r in db_results:
            f.write(r.artist_name + ',' + r.tag_name + ',' + str(r.tag_count_pct) + '\n')

        f.close()


    def get_related_tags(self):
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
        ORDER BY x.score ASC
        '''

        # get the results of above query
        db_results =  self.engine.execute(raw_sql)

        # Create a tuple-dict for DISTINCT results
        distinct_results = {}
        for r in db_results:
            tpl = ( r.t1 , r.t2 ) 
            inv_tpl = ( r.t2 , r.t1 ) 

            try:
                distinct_results[inv_tpl]
            except KeyError:
                distinct_results[tpl] = r.score

        # Find the Max Score (to normalize btwn 0 and 1)
        # JD:  There has gotta be a better way to do this :-/ 
        max_key = max(distinct_results,key=distinct_results.get)
        max_value = distinct_results[max_key]

        f = open('related_tags.txt', 'w+')

        #write the header
        f.write('tag_1, tag_2, score')

        for tag_combo,score in sorted(distinct_results.items()):
            print tag_combo, score / max_value

            #ensure the score is between 0 and 1
            score_normal = ( score / max_value ) 
            # write the output to a file
            f.write(tag_combo[0] + ','  + tag_combo[1] + ',' +  str(score_normal) + '\n')

        f.close()

        # output each line to a text file

        #
        # f.write('artist_name, tag_name, tag_count_pct\n')

        # for r in db_results:
        #     f.write(r.t1 + ',' + r.t2 + ',' + str(r.score) + '\n')

        # f.close()



if __name__ == "__main__":
    t = DbTask()
    t.get_related_tags()







