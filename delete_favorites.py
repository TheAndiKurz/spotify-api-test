import yaml

with open("conf.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

client_id = config["client_id"]
client_secret = config["client_secret"]


import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:5173/callback",
        scope="user-library-read playlist-read-private user-library-modify playlist-modify-private playlist-modify-public",
    )
)

results = sp.current_user_saved_tracks(limit=50)

tracks = []

for idx, item in enumerate(results["items"]):
    track = item["track"]
    tracks.append(track)


offset = 50
while offset < results["total"]:
    results = sp.current_user_saved_tracks(limit=50, offset=offset)
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        tracks.append(track)

    offset += 50

# remove every track from saved songs
offset = 0
while offset < len(tracks):
    sp.current_user_saved_tracks_delete(
        [track["id"] for track in tracks[offset : offset + 50]]
    )
    offset += 50
