#!/usr/bin/env python
# coding: utf-8

# In[1]:


import configparser


# In[2]:


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')


# In[3]:


# DROP TABLES
# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender CHAR(1),
    itemInSession INTEGER,
    lastName VARCHAR,
    length FLOAT,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration FLOAT,
    sessionId INTEGER,
    song VARCHAR,
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR,
    userId INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    num_songs INTEGER,
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration NUMERIC,
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id int IDENTITY(0,1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL, 
    user_id INTEGER NOT NULL, 
    level VARCHAR, 
    song_id VARCHAR, 
    artist_id VARCHAR, 
    session_id INTEGER, 
    location VARCHAR, 
    user_agent VARCHAR);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int NOT NULL PRIMARY KEY, 
    first_name VARCHAR NOT NULL, 
    last_name VARCHAR NOT NULL, 
    gender CHAR, 
    level VARCHAR);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR NOT NULL PRIMARY KEY, 
    song_title VARCHAR NOT NULL, 
    artist_id VARCHAR NOT NULL, 
    year INTEGER, 
    duration NUMERIC);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR NOT NULL PRIMARY KEY, 
    artist_name VARCHAR NOT NULL, 
    location VARCHAR, 
    latitude FLOAT, 
    longitude FLOAT);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP NOT NULL PRIMARY KEY, 
    hour INTEGER, 
    day INTEGER, 
    week INTEGER, 
    month INTEGER, 
    year INTEGER, 
    weekday INTEGER);
""")


# In[6]:


# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    iam_role {}
    region 'us-west-2'
    json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
    copy staging_songs from {}
    iam_role {}
    region 'us-west-2' json 'auto';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])


# In[7]:



# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT CAST(TIMESTAMP 'epoch' + se.ts/1000 * interval '1 second' as timestamp) AS start_time,
    se.userId, se.level, ss.song_id, ss.artist_id, se.sessionId, se.location, se.userAgent
FROM staging_events AS se 
INNER JOIN staging_songs AS ss ON se.song = ss.title
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT distinct  userId, firstName, lastName, gender, level
FROM staging_events
WHERE page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs(song_id, song_title, artist_id, year, duration)
SELECT song_id, title, artist_id, year, duration
FROM staging_songs
WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, artist_name, location, latitude, longitude)
SELECT distinct artist_id, artist_name, artist_location , artist_latitude, artist_longitude 
FROM staging_songs
WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
SELECT  start_time,
        EXTRACT(hour from start_time), EXTRACT(day from start_time),
        EXTRACT(week from start_time), EXTRACT(month from start_time),
        EXTRACT(year from start_time), EXTRACT(dayofweek from start_time)
FROM songplays;
""")


# In[8]:


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

