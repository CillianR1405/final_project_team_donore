import sqlite3
import os
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np




def get_db_connection():

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "music_database", "music.db")
    return sqlite3.connect(db_path)





def spotify_popularity():
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


def get_itunes_price():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT trackPrice
        FROM itunesTracks
        WHERE trackPrice is NOT NULL;

    """)


    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows


def get_avg_itunes_price_genre():
    conn = get_db_connection()
    cur = conn.cursor()


    cur.execute("""
        SELECT genre, AVG(trackPrice) as avg_price
        FROM itunesTracks
        WHERE trackPrice IS NOT NULL AND genre IS NOT NULL
        GROUP BY genre
        ORDER BY avg_price DESC;
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

def plot_avg_itunes_price_genre():
    data = get_avg_itunes_price_genre()

    if not data:
        print("No iTunes data available.")
        return

    genres = [row[0] for row in data]
    avg_prices = [row[1] for row in data]

    plt.figure(figsize=(10, 5))
    plt.bar(genres, avg_prices, color="orange", edgecolor="black")

    plt.xlabel("Genre")
    plt.ylabel("Average Track Price ($)")
    plt.title("Average iTunes Track Price per Genre")
    plt.yticks(np.arange(0.7, 1.31, 0.1))

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()


    


def plot_spotify_pop():

    my_data = spotify_popularity()

    if not my_data:
        print("Spotify data is unavailable")
        return 

    artists = [row[0] for row in my_data]
    popularity = [row[1] for row in my_data]

    plt.figure(figsize=(12, 6))
    plt.bar(artists, popularity, color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Average Popularity")
    plt.title("Average Spotify Popularity per Artist")
    plt.tight_layout()
    plt.show()


def plot_spotify_popularity_histogram():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""SELECT popularity 
            FROM spotifyTracks  
            WHERE popularity IS NOT NULL;
    """)
    
    
    
    
    pops = [row[0] for row in cur.fetchall()]
    conn.close()

    plt.figure(figsize=(10, 5))
    plt.hist(pops, bins=10, color="green", edgecolor="black")
    plt.xlabel("Popularity")
    plt.ylabel("Number of Songs")
    plt.title("Distribution of Spotify Track Popularity")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    plot_spotify_pop()
    plot_spotify_popularity_histogram()
    plot_avg_itunes_price_genre()
