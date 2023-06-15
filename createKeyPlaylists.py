from client import Track, SpotifyClient
import time
import logging

THROTTLING_BUFFER = 1.5  # secs


def get_key(client, track_id):
    features = client.client.audio_features(track_id)

    track_features = features[0]

    key_number = track_features['key']
    mode_number = track_features['mode']
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    modes = ['m', '']
    key_name = keys[key_number] + modes[mode_number] + 'test'
    return key_name


def get_playlist_tracks(client, playlist_id):
    # Get the track IDs from the playlist
    results = client.client.playlist_tracks(playlist_id, fields='items.track.id,total', limit=100)

    tracks = []
    total = results['total']
    while len(tracks) < total:
        results = client.client.playlist_tracks(playlist_id, fields='items.track,total', limit=100, offset=len(tracks))
        for item in results['items']:
            try:
                track_name = item['track']['name']
                track_id = item['track']['id']
                track_main_artist = item['track']['artists'][0]['name']
                track_key = get_key(client, item['track']['id'])
                track = Track(track_name, track_id, track_main_artist, track_key)
                tracks.append(track)
            except TypeError as e:
                logging.error("Error occurred while retrieving track features: %s", str(e))
                pass
        break
    
    return tracks

def populate_playlist_helper(client, playlist, tracks):
    if len(tracks) <= 100:
        client.populate_playlist(playlist, tracks)
    else:
        # Split the list into chunks of 100 elements or less
        chunk_size = 100
        chunks = [tracks[i:i+chunk_size] for i in range(0, len(tracks), chunk_size)]
        
        for chunk in chunks:
            client.populate_playlist(playlist, chunk)

def create_key_playlists(client, tracks):
    song_keys = dict()
    for track in tracks:
        try:
            song_key = track.key
        except Exception as e:
            print("exception in : ", e)
            continue
        song_keys[song_key] = song_keys.get(song_key, []) + [track]

    for k in song_keys:
        # Create playlist named after the song key, k
        playlist = client.create_playlist(k)

        # Populate that playlist with songs in the key of k
        populate_playlist_helper(client, playlist, song_keys[k])
        time.sleep(THROTTLING_BUFFER)


def main(client_id, client_secret, redirect_uri, user_id, playlist_id):
    default_client = SpotifyClient(client_id, client_secret, redirect_uri, user_id)
    playlist_creation_client = SpotifyClient(client_id, client_secret, redirect_uri, user_id, scope='playlist-modify-public')
    tracks = get_playlist_tracks(default_client, playlist_id)
    create_key_playlists(playlist_creation_client, tracks)
