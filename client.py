import json
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# This file is largely adapted from https://github.com/musikalkemist/spotifyplaylistgenerator/blob/master/spotifyclient.py

class Track:

    def __init__(self, name, id, artist, key):
        """
        name : str 
            Track name
        id : int
            Spotify track id
        artist : str
            Artist who wrote the track
        """
        self.name = name
        self.id = id
        self.artist = artist
        self.key = key

    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return self.name + " by " + self.artist

class Playlist:

    def __init__(self, name, id):
        """
        name : str 
            Playlist name
        id : int 
            Spotify playlist id
        """
        self.name = name
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}"

class SpotifyClient:

    def __init__(self, client_id, client_secret, redirect_uri, user_id, scope='user-read-private'):
        """
        authorization_token : str
            Spotify API token
        param user_id : str
            Spotify user id
        """
        self.client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope
                                                ))
        self.user_id = user_id
        self.authorization_token = self.get_access_token(client_id, client_secret, redirect_uri, scope)


    def get_access_token(self, client_id, client_secret, redirect_uri, scope):
        token_info = self.client.auth_manager.get_access_token()
        return token_info['access_token']


    def create_playlist(self, name):
        """
        name : str
            New playlist name
        playlist : Playlist
            Newly created playlist
        """
        data = json.dumps({
            "name": name,
            "description": "",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self._place_post_api_request(url, data)
        response_json = response.json()

        # create playlist
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        """
        playlist : Playlist obj
            Playlist to which to add tracks
        tracks : list: 
            List of Track objs to be added to our playlist

        returns
        ------------------
        API response
        """
        # track_uris = [track.create_spotify_uri() for track in tracks]
        track_uris = []
        for track in tracks:
            try:
                track_uris.append(track.create_spotify_uri())
            except:
                print(f"Couldn't produce uri for track {track.name}")
                continue
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data)
        response_json = response.json()
        print(response_json)
        return response_json

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.authorization_token}"
            }
        )
        return response
