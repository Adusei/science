
## THIS IS MY DATABASE SCHEMA THAT I DEFINED DIRECTLY IN MYSQL

#server = localhost; DB = last_fm ; u=root ; p=

##################
### TAGS TABLE ###
##################

CREATE TABLE tags
(
    tag_id INT PRIMARY KEY AUTO_INCREMENT
    ,tag_name NVARCHAR(255)
--  ,last_fm_tag_uid;
);

CREATE UNIQUE INDEX t_n_ix on tags ( tag_name );

#####################
### ARTISTS TABLE ###
#####################

CREATE TABLE artists
(
    artist_id INT PRIMARY KEY AUTO_INCREMENT
    ,artist_name NVARCHAR(255)
--  ,last_fm_artist_uid;
);

CREATE UNIQUE INDEX a_n_ix on artists ( artist_name );

#############################
### ARTISTS TO TAGS TABLE ###
#############################

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

