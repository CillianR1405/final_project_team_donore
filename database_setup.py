import sqlite3
import os

base_directory = os.path.dirname(os.path.abspath(__file__))
database_folder = os.path.join(base_directory, "music_database")
os.makedirs(database_folder, exist_ok=True)
database_path = os.path.join(database_folder, "music.db")

conn = sqlite3.connect(database_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS spotify_artists (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS spotifyTracks (
    id TEXT PRIMARY KEY,
    name TEXT,
    artistId TEXT,
    popularity INTEGER,
    duration INTEGER,
    albumTitle TEXT,
    releaseDate TEXT,
    FOREIGN KEY (artistId) REFERENCES spotifyArtists(id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS itunesTracks (
    trackId INTEGER PRIMARY KEY,
    name TEXT,
    artist TEXT,
    genre TEXT,
    releaseDate TEXT,
    trackPrice REAL,
    collectionPrice REAL,
    duration INTEGER
)
""")

conn.commit()
conn.close()

print("Created database")