import sqlite3
import requests
import os


TOKEN = "BQDdCg_Bnso5BB0rFus1gpOqtiJEo-cMpp_G-uEw49bf0xJBWP5ZOxzJK1b_THcNKfFX_F-HcSeWt8TptyujuQAOQzVDR5urFfkC27crtmnToWCtvoY3dod1U1vcJX4q8QDWPDT-yiM"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}




def get_db_connection():
   base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   db_path = os.path.join(base_dir, "music_database", "music.db")
   return sqlite3.connect(db_path)


def store_spotify_by_genre(genre="jazz"):
   conn = get_db_connection()
   cur = conn.cursor()


   search_url = "https://api.spotify.com/v1/search"
   search_params = {
       "q": f"genre:{genre}",
       "type": "artist",
       "limit": 10
   }


   response = requests.get(search_url, headers=HEADERS, params=search_params)
   data = response.json()


   if "artists" not in data:
       print("Error retrieving artists:", data)
       conn.close()
       return


   artists = data["artists"]["items"]
   track_storage = 0
   max_tracks = 25


   for artist in artists:
       if track_storage >= max_tracks:
           break


       artist_id = artist["id"]
       artist_name = artist["name"]




       cur.execute(
           "INSERT OR IGNORE INTO spotifyArtists (id, name) VALUES (?, ?)",
           (artist_id, artist_name)
       )


       tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
       track_resp = requests.get(tracks_url, headers=HEADERS, params={"market": "US"})
       track_data = track_resp.json()


       if "tracks" not in track_data:
           continue


       for t in track_data["tracks"]:
           if track_storage >= max_tracks:
               break


           track_id = t["id"]
           track_name = t["name"]
           popularity = t["popularity"]
           duration = t["duration_ms"]
           album_title = t["album"]["name"]
           release_date = t["album"]["release_date"]


           cur.execute("SELECT id FROM spotifyTracks WHERE id = ?", (track_id,))
           if cur.fetchone():
               print(f"Skipped duplicate: {track_name}")
               continue


           cur.execute("""
               INSERT INTO spotifyTracks
               (id, name, artistId, popularity, duration, albumTitle, releaseDate)
               VALUES (?, ?, ?, ?, ?, ?, ?)
           """, (
               track_id, track_name, artist_id, popularity,
               duration, album_title, release_date
           ))


           track_storage += 1
           print(f"Inserted: {track_name} ({artist_name})")


   conn.commit()
   conn.close()
   print(f"\nStored {track_storage} tracks for genre '{genre}'")
  


if __name__ == "__main__":
   
   genres = ["house", "pop", "jazz", "rap", "electronic"]
   
   for genre in genres:
      store_spotify_by_genre(genre)