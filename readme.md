# Spotify Api Test

This is a simple test of the Spotify Api. It uses the Spotipy library to make requests to the Spotify Api.

It can be used to backup your saved tracks, delete all your saved tracks and add to your saved tracks from a intersection of two playlists.

## How to use

you need to create a spotify app in your Spotify developer dashboard. You can find the dashboard [here](https://developer.spotify.com/dashboard).

You also need to set your redirect uri to `http://localhost:5173/callback` in your app settings.

Create a conf.yaml file in the root of the project with the following content:

```yaml
client_id: <your client id>
client_secret: <your client secret>
```

You can find the client id and client secret in your app settings.