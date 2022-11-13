create_tracks_table = """
    CREATE TABLE IF NOT EXISTS tracks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_track VARCHAR(50) UNIQUE,
        artist_name VARCHAR(50),
        track_name VARCHAR(50)
    );
"""

create_plays_table = """
    CREATE TABLE IF NOT EXISTS plays(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user VARCHAR(50),
        id_track VARCHAR(50),
        date VARCHAR(50),
        CONSTRAINT fk_tracks
            FOREIGN KEY (id_track)
            REFERENCES tracks(id_track)
    )
"""

insert_track = 'INSERT OR IGNORE INTO tracks(id_track, artist_name, track_name) VALUES(?,?,?)'
insert_play = 'INSERT INTO plays(id_user, id_track, date) VALUES(?,?,?)'

select_popular_artist = """
    SELECT tracks.artist_name, COUNT(*) as counted_plays
    FROM plays
    LEFT JOIN tracks ON plays.id_track=tracks.id_track
    GROUP BY artist_name
    ORDER BY counted_plays DESC
    LIMIT 1;
"""

select_popular_tracks = """
    SELECT tracks.id_track, artist_name, track_name, COUNT(*) as counted_plays
    FROM tracks
    INNER JOIN plays ON tracks.id_track=plays.id_track
    GROUP BY tracks.id_track
    ORDER BY counted_plays DESC
    LIMIT 5;
"""