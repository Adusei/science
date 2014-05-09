# last_db.py

from __future__ import absolute_import
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
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
        try:
            artist_ins = artist_table.insert()
            self.engine.execute(artist_ins,artist_name = artist_name)
            print '...success fully insertest tag!!' + artist_name
        except IntegrityError:
            pass

        self.db_session.close()
        # http://stackoverflow.com/questions/8585346/get-last-inserted-value-from-mysql-using-sqlalchemy    
        ## DO THIS BEFORE HANDING IN THE CODE... WHAT IS BELOW IS GARBAGE ##


    def get_tag_by_name (self, tag_name):
        tags_table = al.Table('tags', self.metadata, autoload=True)

        where_clause = "tag_name = '" + tag_name + "'"
        s = tags_table.select().where(where_clause)

        rs = s.execute()

        for r in rs:
            tag_id = r.tag_id
            print tag_id
        
        self.db_session.close()
        return rs


    def get_artist_by_name(self, artist_name):
        artist_table = al.Table('artists', self.metadata, autoload=True)

        where_clause = "artist_name = '" + artist_name + "'"
        s = artist_table.select().where(where_clause) #.limit(1)
        # Since there is a unique index on artist_name dont need to limit

        rs = s.execute()

        for r in rs:
            artist_id = r.artist_id
            print artist_id
        
        self.db_session.close()
        return rs



if __name__ == "__main__":
    t = DbTask()
    t.get_tag_by_name("a")
    # t.



'''
# I SHOULD DEFINE THIS VIA SQL ALCHEMY
# BUT I DID THIS DIRECTLY IN MYSQL FOR NOW

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



