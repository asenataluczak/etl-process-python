from argparse import ArgumentParser
from functools import wraps
from sqlite3 import connect
import sql_queries
import time

# how to run:
# python main.py --db='test.sql' --tracks='unique_tracks.txt' --plays='triplets_sample_20p.txt' --amount_of_plays=100

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total = end - start
        print(f"""
            [Czas przetwarzania danych: {total:.4f} sekund]""")
        return result
    return wrapper


@timeit
def save_to_db(db, tracks, plays, amount_of_plays):
    with connect(db) as db_connector:
        db_connector.execute(sql_queries.create_tracks_table)
        db_connector.execute(sql_queries.create_plays_table)
        db_cursor = db_connector.cursor()

        # Insert tracks into db
        tracks_db = []
        tracks_file = open(tracks, 'r', errors="ignore")
        for track in tracks_file.readlines():
            track = track.strip().split('<SEP>')
            track.pop(0)
            tracks_db.append(track)
        db_cursor.executemany(sql_queries.insert_track, tracks_db)
        db_connector.commit()
        tracks_file.close()

        # Insert plays into db
        plays_db = []
        plays_file = open(plays, 'r', errors="ignore")
        plays = plays_file.readlines()
        plays_length = amount_of_plays or len(plays)
        for i in range(plays_length):
            plays[i] = plays[i].strip().split('<SEP>')
            plays_db.append(plays[i])
        db_cursor.executemany(sql_queries.insert_play, plays_db)
        db_connector.commit()
        plays_file.close()

        # Get and display results
        res_artist = db_cursor.execute(sql_queries.select_popular_artist)
        artist_name, artist_plays = res_artist.fetchone()
        res_tracks = db_cursor.execute(sql_queries.select_popular_tracks)
        result = f"""
            ============= NAJPOPULARNIEJSZY ARTYSTA =============
            1. {artist_name}
            liczba odsluchan: {artist_plays}

            ============= NAJPOPULARNIEJSZE UTWORY =============="""

        print(result)
        for i, track in enumerate(res_tracks.fetchall()):
            print(f"""
            {i+1}. {track[2]} ({track[1]})
            liczba odsluchan: {track[3]}""")
    return


def main():
    parser = ArgumentParser()
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--tracks', type=str, required=True)
    parser.add_argument('--plays', type=str, required=True)
    parser.add_argument('--amount_of_plays', type=int)
    args = parser.parse_args()

    save_to_db(args.db, args.tracks, args.plays, args.amount_of_plays)
    input("\n...")


if __name__ == '__main__':
    main()
