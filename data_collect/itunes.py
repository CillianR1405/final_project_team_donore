import requests
import sqlite3
import os

def connect_database():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base, "music_database", "music.db")
    return sqlite3.connect(data_path)

def get_tracks(term="house", limit=25):
    url = "https://itunes.apple.com/search"
    params = {
        "term": term,
        "entity": "song",
        "limit": limit
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

def store_itunes_data(term="house"):
    conn = connect_database()
    cur = conn.cursor()
    tracks = get_tracks(term=term, limit=25)
    new_tracks = 0

    for track in tracks:
        track_id = track.get("trackId")
        if not track_id:
            continue

        name = track.get("trackName")
        artist = track.get("artistName")
        genre = track.get("primaryGenreName")
        release_date = track.get("releaseDate")
        track_price = track.get("trackPrice")
        collection_price = track.get("collectionPrice")
        duration_ms = track.get("trackTimeMillis")

        cur.execute(
            """
            INSERT OR IGNORE INTO itunes_tracks
                (track_id, name, artist, genre, release_date,
                 track_price, collection_price, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                track_id,
                name,
                artist,
                genre,
                release_date,
                track_price,
                collection_price,
                duration_ms
            )
        )

        if cur.rowcount > 0:
            new_tracks += 1

    conn.commit()
    conn.close()

if __name__ == "__main__":
    terms = ["house", "rap", "pop", "jazz"]
    for term in terms:
        store_itunes_data(term)