import yaml

import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("conf.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

playlist_count_to_insert = int(sys.argv[1])

client_id = config["client_id"]
client_secret = config["client_secret"]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:5173/callback",
        scope="user-library-read playlist-read-private user-library-modify",
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

results = sp.current_user_playlists()

monthly_playlists = {}

for playlist1 in results["items"]:
    if len(playlist1["name"]) == 6 and playlist1["name"].isdigit():
        monthly_playlists[playlist1["name"]] = {
            "id": playlist1["id"],
        }


for playlist1 in monthly_playlists:
    results = sp.playlist_tracks(monthly_playlists[playlist1]["id"], limit=100)
    tracks = []
    for track in results["items"]:
        tracks.append(track["track"]["id"])
    offset = 100

    while offset < results["total"]:
        results = sp.playlist_tracks(
            monthly_playlists[playlist1]["id"], limit=100, offset=offset
        )
        for track in results["items"]:
            tracks.append(track["track"]["id"])
        offset += 100

    monthly_playlists[playlist1]["tracks"] = set(tracks)


# count the times the traks where in a monthly playlist
track_counter = {}
for playlist_name, playlist in monthly_playlists.items():
    for track in playlist["tracks"]:
        if track not in track_counter:
            track_counter[track] = 0

        track_counter[track] += 1


# get names of the tracks
favorit_ids = []
for track_id, count in track_counter.items():
    if count >= playlist_count_to_insert:
        favorit_ids.append(track_id)


# get the name of the intersecting track ids
favorits = [sp.track(id) for id in favorit_ids]

# add the tracks to the user's library
for track in favorits:
    if sp.current_user_saved_tracks_contains([track["id"]])[0]:
        continue
    print(f"Adding {track['name']} to saved tracks")
    sp.current_user_saved_tracks_add([track["id"]])
