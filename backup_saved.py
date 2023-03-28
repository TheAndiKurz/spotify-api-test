import yaml

with open("conf.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

client_id = config["clientID"]
client_secret = config["clientSecret"]


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

# get user playlist with name 202203
playlist_id = ""
playlists = sp.current_user_playlists()
for playlist in playlists["items"]:
    if playlist["name"] == "202203":
        playlist_id = playlist["id"]
        break

offset = 0
while offset < len(tracks):
    sp.playlist_remove_all_occurrences_of_items(
        playlist_id,
        [track["id"] for track in tracks[offset : offset + 100]],
    )

    sp.playlist_add_items(
        playlist_id,
        [track["id"] for track in tracks[offset : offset + 100]],
    )
    offset += 100
