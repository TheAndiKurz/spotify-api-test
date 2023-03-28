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


# get the intersection of all the playlists
intersections = {}
for name1, playlist1 in monthly_playlists.items():
    for name2, playlist2 in monthly_playlists.items():
        if name1 == name2:
            continue

        num1 = int(name1)
        num2 = int(name2)

        if num1 > num2:
            continue

        if abs(num1 - num2) != 1:
            continue

        intersections[(name1, name2)] = set.intersection(
            playlist1["tracks"],
            playlist2["tracks"],
        )


# get the name of the intersecting track ids
intersection_tracks = []

for name, intersection in intersections.items():
    results = sp.tracks(intersection)
    intersection_tracks.extend(results["tracks"])


# add the tracks to the user's library
for track in intersection_tracks:
    if sp.current_user_saved_tracks_contains([track["id"]])[0]:
        continue
    print(f"Adding {track['name']} to saved tracks")
    sp.current_user_saved_tracks_add([track["id"]])
