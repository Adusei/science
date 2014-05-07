# last_db.py
from __future__ import absolute_import
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

import sqlalchemy as al



class DbTask(object):
    # ensures the connection the the database is closed on task completion
    db_connection_string  = 'mysql://root@localhost/last_fm'


    engine = create_engine(db_connection_string, convert_unicode=True,pool_recycle=3600, pool_size=20)
    engine.echo = False
    db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))

    metadata = al.MetaData(engine)

    abstract = True

    def __init__(self):
        print("Initializing DBTask!")

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.close()

    def add_artist (self, artist_name):
        artist_table = al.Table('artists', self.metadata, autoload=True)
        try:
            artist_ins = artist_table.insert()
            self.engine.execute(artist_ins,artist_name = artist_name)
            print '...success fully insertest tag!!' + artist_name
        except IntegrityError:
            pass
        
        self.db_session.close()

if __name__ == "__main__":
    t = DbTask()
    t.add_artist("raresh")


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



