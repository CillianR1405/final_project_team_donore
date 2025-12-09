import sqlite3
import os


def get_db_connection():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "music_database", "music.db")
    return sqlite3.connect(db_path)


def spotify_popularity_by_artist():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT a.name, AVG(t.popularity) AS avg_pop
    FROM spotify_artists AS a
    JOIN spotifyTracks AS t
        ON a.id = t.artistId
    GROUP BY a.id
    ORDER BY avg_pop DESC;
    """

    rows = cur.execute(query).fetchall()
    conn.close()
    return rows


def avg_itunes_price_genre():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT genre, AVG(trackPrice) AS avg_price
    FROM itunesTracks
    WHERE trackPrice IS NOT NULL
    GROUP BY genre
    ORDER BY avg_price DESC;
    """

    rows = cur.execute(query).fetchall()
    conn.close()
    return rows


def show_results():
    print("Average Spotify Popularity per Artist\n")
    for name, popularity in spotify_popularity_by_artist():
        print(f"{name}: {popularity}")

    print("\nAverage iTunes Track Price per Genre\n")
    for genre, price in avg_itunes_price_genre():
        print(f"{genre}: ${price}")


if __name__ == "__main__":
    show_results()
