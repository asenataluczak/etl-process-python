from functools import wraps
from sqlite3 import connect
import sql_queries
import time


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


def extract(file):
    file = open(file, 'r', errors="ignore")
    rows = file.readlines()
    file.close()
    return rows


def transform(file, limit = 0):
    data_db = []
    rows = extract(file)
    length = limit or len(rows)
    for i in range(length):
        rows[i] = rows[i].strip().split('<SEP>')
        if (bool(limit) == False):
            rows[i].pop(0)
        data_db.append(rows[i])
    return data_db


@timeit
def etl(db, tracks, plays, amount_of_plays):
    transformed_tracks = transform(tracks)
    transformed_plays = transform(plays, amount_of_plays)

    with connect(db) as db_connector:
        # Load data 
        db_connector.execute(sql_queries.create_tracks_table)
        db_connector.execute(sql_queries.create_plays_table)
        db_cursor = db_connector.cursor()

        db_cursor.executemany(sql_queries.insert_track, transformed_tracks)
        db_connector.commit()
        db_cursor.executemany(sql_queries.insert_play, transformed_plays)
        db_connector.commit()
        
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