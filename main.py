from argparse import ArgumentParser
from sqlite3 import connect

# how to run:
# python main.py --db='test.sql' --tracks='unique_tracks.txt' --plays='triplets_sample_20p.txt' --amount_of_plays=100

create_tracks_table = """
    CREATE TABLE IF NOT EXISTS tracks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_track VARCHAR(50),
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

insert_track = 'INSERT INTO tracks(id_track, artist_name, track_name) VALUES(?,?,?)'
insert_play = 'INSERT INTO plays(id_user, id_track, date) VALUES(?,?,?)'

get_popular_artist = """
    SELECT artist_name, COUNT(*) as counted_plays
    FROM tracks 
    INNER JOIN plays ON tracks.id_track=plays.id_track
    GROUP BY artist_name
    ORDER BY counted_plays DESC
    LIMIT 1;
"""


def save_to_db(db, tracks, plays, amount_of_plays):
    with connect(db) as db_connector:
        db_connector.execute(create_tracks_table)
        db_connector.execute(create_plays_table)
        db_cursor = db_connector.cursor()

        # Insert tracks into db
        tracks_db = []
        tracks_file = open(tracks, 'r', errors="ignore")
        for track in tracks_file.readlines():
            track = track.strip().split('<SEP>')
            track.pop(0)
            tracks_db.append(track)
        db_cursor.executemany(insert_track, tracks_db)
        tracks_file.close()

        # Insert plays into db
        plays_db = []
        plays_file = open(plays, 'r', errors="ignore")
        plays = plays_file.readlines()
        plays_length = amount_of_plays or len(plays)
        for i in range(plays_length):
            plays[i] = plays[i].strip().split('<SEP>')
            plays_db.append(plays[i])
        db_cursor.executemany(insert_play, plays_db)
        plays_file.close()
    return


def main():
    parser = ArgumentParser()
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--tracks', type=str, required=True)
    parser.add_argument('--plays', type=str, required=True)
    parser.add_argument('--amount_of_plays', type=int)
    args = parser.parse_args()

    save_to_db(args.db, args.tracks, args.plays, args.amount_of_plays)
    input()


if __name__ == '__main__':
    main()
