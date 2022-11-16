create_tracks_table = """
    CREATE TABLE IF NOT EXISTS tracks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_track VARCHAR(20) UNIQUE,
        artist_name VARCHAR(40),
        track_name VARCHAR(50)
    );
"""

create_plays_table = """
    CREATE TABLE IF NOT EXISTS plays(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user VARCHAR(40),
        id_track VARCHAR(20),
        date VARCHAR(15),
        CONSTRAINT fk_tracks
            FOREIGN KEY (id_track)
            REFERENCES tracks(id_track)
    )
"""

insert_track = 'INSERT OR IGNORE INTO tracks(id_track, artist_name, track_name) VALUES(?,?,?)'
insert_play = 'INSERT INTO plays(id_user, id_track, date) VALUES(?,?,?)'

helper_view = """
    CREATE VIEW plays_view 
    AS SELECT id_track, COUNT(id_track) AS 'counted_plays' 
    FROM plays 
    GROUP BY id_track 
    ORDER BY COUNT(id_track) DESC;
"""

limited_helper_view = """
    CREATE VIEW limited_plays_view 
    AS SELECT * FROM plays_view 
    LIMIT 5;
"""

select_popular_tracks = """
    SELECT tracks.track_name, tracks.artist_name, limited_plays_view.counted_plays 
    FROM limited_plays_view 
    LEFT JOIN tracks ON tracks.id_track=limited_plays_view.id_track;
"""

select_popular_artist = """
    SELECT tracks.artist_name, SUM(plays_view.counted_plays)
    FROM plays_view 
    LEFT JOIN tracks ON tracks.id_track=plays_view.id_track 
    GROUP BY tracks.artist_name 
    ORDER BY SUM(plays_view.counted_plays) DESC
    LIMIT 1;
"""
