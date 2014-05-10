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


    def get_related_tags(self):
        raw_sql = '''select 
        t1.tag_name as t1 , t2.tag_name as t2, x.c
        from 
        (
            select
                at_1.tag_id as tag_id_1
                , at_2.tag_id as tag_id_2
                , count(*) as c
            from artist_to_tags at_1
                inner join artist_to_tags at_2
                on at_1.artist_id = at_2.artist_id
                and at_1.tag_id != at_2.tag_id
            GROUP BY at_1.tag_id, at_2.tag_id HAVING COUNT(*) > 10
        ) x
        inner join tags t1
            on x.tag_id_1 = t1.tag_id
        inner join tags t2
            on x.tag_id_2 = t2.tag_id
        ORDER BY x.c desc'''

        db_results =  self.engine.execute(raw_sql)

        for r in db_results:
            print r.t1 + ' | ' + r.t2 
            # print 



if __name__ == "__main__":
    t = DbTask()
    t.get_related_tags()
    t.set_tag_pct(4154,1000)


'''
## THIS IS MY DATABASE SCHEMA THAT I DEFINED DIRECTLY IN MYSQL

#DB = last_fm ; u=root ; p=

### TAGS TABLE ###
CREATE TABLE tags
(
    tag_id INT PRIMARY KEY AUTO_INCREMENT
    ,tag_name NVARCHAR(255)
--  ,last_fm_tag_uid;
);

CREATE UNIQUE INDEX t_n_ix on tags ( tag_name );

### ARTISTS TABLE ###

CREATE TABLE artists
(
    artist_id INT PRIMARY KEY AUTO_INCREMENT
    ,artist_name NVARCHAR(255)
--  ,last_fm_artist_uid;
);

CREATE UNIQUE INDEX a_n_ix on artists ( artist_name );

### ARTISTS TO TAGS TABLE ###

CREATE TABLE artist_to_tags
(
    artist_id INT
    ,tag_id INT
    ,tag_count INT
    ,tag_count_pct FLOAT
    ,PRIMARY KEY (artist_id,tag_id)
    ,FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
    ,FOREIGN KEY (tag_id) REFERENCES tags(tag_id)

);


'''



