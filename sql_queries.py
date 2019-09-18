import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= """
CREATE TABLE staging_events (
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender VARCHAR,
    itemInSession INT,
    lastName VARCHAR,
    length NUMERIC,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration VARCHAR,
    sessionId INT,
    song VARCHAR,
    status INT,
    ts BIGINT,
    userAgent VARCHAR,
    userId INT
    );
"""

staging_songs_table_create = """
CREATE TABLE staging_songs (
    num_songs INT,
    artist_id VARCHAR,
    artist_latitude NUMERIC,
    artist_longitude NUMERIC,
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration NUMERIC,
    year INT
    );
"""

songplay_table_create = """
CREATE TABLE songplays (
    songplay_id INT IDENTITY(0,1) PRIMARY KEY,
    starttime TIMESTAMP,
    user_id INT NOT NULL,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR
  );
"""

user_table_create = """
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender VARCHAR,
    level VARCHAR
  );
"""

song_table_create = """
CREATE TABLE songs (
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR,
    year INT,
    duration NUMERIC
  );
"""

artist_table_create = """
CREATE TABLE artists (
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR,
    latitude NUMERIC,
    longitude NUMERIC
  );
"""

time_table_create = """
CREATE TABLE time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday VARCHAR
  );
"""

# STAGING TABLES

staging_events_copy = """
    COPY staging_events
    FROM {}
    IAM_ROLE {}
    JSON AS {}
    REGION 'us-west-2'
    """.format(config.get('S3', 'LOG_DATA'),
               config.get('IAM_ROLE', 'ARN'),
               config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = """
COPY staging_songs
    FROM {}
    IAM_ROLE {}
    JSON AS 'auto'
    REGION 'us-west-2'
    """.format(config.get('S3', 'SONG_DATA'),
               config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = """
INSERT INTO songplays (
  starttime,
  user_id, 
  level, 
  song_id, 
  artist_id, 
  session_id, 
  location, 
  user_agent 
)
SELECT 
  timestamp 'epoch' + ts/1000 * interval '1 second' as starttime,
  userid as user_id,
  level,
  song_id,
  artist_id,
  sessionid as session_id,
  location,
  useragent as user_agent
FROM
  staging_events as e
JOIN
  staging_songs as s
ON
  s.artist_name=e.artist AND e.song=s.title
WHERE
  e.page = 'NextSong'
"""

user_table_insert = """
INSERT INTO users (
  user_id,
  first_name,
  last_name,
  gender,
  level
)
SELECT
  DISTINCT userid,
  firstname,
  lastname,
  gender,
  level
FROM
  staging_events
WHERE
  userid IS NOT NULL
"""

song_table_insert = """
INSERT INTO songs (
  song_id,
  title,
  artist_id,
  year,
  duration 
)
SELECT
  DISTINCT song_id,
  title,
  artist_id,
  year,
  duration
FROM
  staging_songs
WHERE
  song_id IS NOT NULL
"""

artist_table_insert = """
INSERT INTO artists (
  artist_id,
  name,
  location,
  latitude,
  longitude 
)
SELECT
  DISTINCT artist_id,
  artist_name,
  artist_location,
  artist_latitude,
  artist_longitude
FROM
  staging_songs
WHERE
  artist_id IS NOT NULL
"""

time_table_insert = """
INSERT INTO time (
  start_time,
  hour,
  day,
  week,
  month,
  year,
  weekday
)
SELECT
  DISTINCT timestamp 'epoch' + ts/1000 * interval '1 second' as start_time,
  EXTRACT(hour FROM start_time) AS hour,
  EXTRACT(day FROM start_time) AS day,
  EXTRACT(week FROM start_time) AS week,
  EXTRACT(month FROM start_time) AS month,
  EXTRACT(year FROM start_time) AS year,
  EXTRACT(dayofweek FROM start_time) AS weekday
FROM
  staging_events;
"""


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
