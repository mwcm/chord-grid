import os
import tekore as tk
from dotenv import load_dotenv

load_dotenv()

# notes
# -----
# - how best to recognize a track from an file and get that info from spotify?
#   - does acousticbrainz have a thing for this?
#   - rely on user input of song name & select from list?
#   - analyze audio_file another way?
# - will the analysis beat/chord/bar/etc times be useful if it's not the exact same file? 
#   - could atleast compare them with our results from madmom & expected results

class Spotify:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.token = tk.request_client_token(self.client_id, self.client_secret)
        self.api = tk.Spotify(self.token)
        return

    def get_track_analysis(self, track):
        return

    def get_track_features(self, track):
        return