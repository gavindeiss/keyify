# Keyify

This script takes all the songs in a specified playlist and breaks them out into 24 more playlists sorted by key and mode.

To run this script, execute the following command in your terminal:

```
python3 main.py --clientId <...> --clientSecret <...> --redirectUri <...> --userId <...> --playlistId <...>
```

The first 3 arguments correspond to information you should be able to access from the spotify API when creating an app, per the instructions (here)[https://developer.spotify.com/documentation/web-api/concepts/apps].

Your userId is simply your spotify user ID.

Playlist ID can be found either by a GET request on playlists listed under your account, or probably more easily, by following the instructions (here)[https://open.spotify.com/playlist/3inHsDf6ADDsvgndEeckkf?si=750d7712a28047b7] 