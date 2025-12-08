import sqlite3
import os

base_directory = os.path.dirname(os.path.abspath(__file__))
database_folder = os.path.join(base_directory, "music_database")
os.makedirs(database_folder, exist_ok=True)
database_path = os.path.join(database_folder, "music.db")
conn = sqlite3.connect(database_path)
cur = conn.cursor()

