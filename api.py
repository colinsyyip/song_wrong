from dotenv import load_dotenv
import json
from random import randint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import time
from tts import play_track_details


def spotify_login(spotify_client_id = None, spotify_client_secret = None, redirect_uri = None):
    scope = "user-read-playback-state,user-modify-playback-state"
    if spotify_client_id is None or spotify_client_secret is None or redirect_uri is None:
        load_dotenv()
        spotify_oauth = SpotifyOAuth(scope = scope)
    else:
        spotify_oauth = SpotifyOAuth(client_id = spotify_client_id,
                                    client_secret = spotify_client_secret,
                                    redirect_uri = redirect_uri,
                                    scope = scope)
    return spotipy.Spotify(client_credentials_manager = spotify_oauth)


def playlist_id_retrieve(name, file_name = "playlists.json"):
    """
    Retrieve playlist dict from file_name.
    """
    f = open(file_name)
    playlist_dict = json.load(f)
    if name not in playlist_dict:
        ValueError("Name not valid - please input one of %s" % playlist_dict.keys())
    return playlist_dict[name]


def get_track_by_index(pl, idx, str_return = True):
    """
    Returns track ID, track name, and artists for a given playlist and index of track within that playlist.
    """
    track_dict = pl['tracks']['items'][idx]['track']
    track_name = track_dict['name']
    artist_list = track_dict['artists']
    track_id = track_dict['id']
    artists = [x['name'] for x in artist_list]
    if str_return:
        artists = ", ".join(artists)

    return {"id": track_id,
            "name": track_name,
            "artist": artists}


def retrieve_devices(sp_obj):
    """
    Returns available device names and IDs known to Spotify.
    """
    available_devices = sp_obj.devices()
    if "devices" not in available_devices:
        print("No devices found.")
        return None
    device_list = available_devices['devices']
    if len(device_list) == 0:
        print("No devices found.")
        return None
    device_id_dict = {x['name']: x['id'] for x in device_list}

    return device_id_dict


def play_track(device_id, track_uri, sp_obj):
    """
    Play specific track_uri on device_id device.
    """
    track_uri_fmt = "spotify:track:%s" % track_uri
    return sp_obj.start_playback(device_id = device_id,
                                 uris = [track_uri_fmt])


def pause_track(device_id, sp_obj):
    """
    Pause specific device_id device.
    """
    return sp_obj.pause_playback(device_id = device_id)


def snippet_playback(snippet_length: int = 15, **kwargs):
    """
    Play track_id for length of snippet_length on given device_id.
    """
    try:
        play_track(**kwargs)
        time.sleep(snippet_length)
        pause_track(device_id = kwargs['device_id'],
                    sp_obj = kwargs['sp_obj'])
    except SpotifyException:
        print("Playback could not be paused. This is either due to playback being paused manually or device disconnection")
    
    return kwargs


def play_snippet_pl(pl_data, sp_obj, snippet_length, to_play_device, info_playback, shuffle, pl_idx: int = 0):
    """
    Play track of given pl for snippet_length on to_play_device. to_play_device is converted to Spotify device id
    """
    num_tracks = len(pl_data['tracks']['items'])
    if shuffle not in (0, 1):
        raise ValueError("shuffle must be either 0 or 1")
    if shuffle == 0:
        if pl_idx >= num_tracks:
            raise ValueError("pl_idx of %.0f exceeds num_tracks of %.0f" % (pl_idx, num_tracks))
        track_idx = pl_idx
    else:
        track_idx = randint(0, num_tracks - 1)
    track_data = get_track_by_index(pl_data, track_idx)
    track_id = track_data['id']
    available_devices = retrieve_devices(sp_obj)
    if to_play_device is None:
        to_play_device_id = available_devices[available_devices.keys()[0]]
    else:
        to_play_device_id = available_devices[to_play_device]
    
    if info_playback == "b":
        track_tuple = (track_data['name'], track_data['artist'])
        play_track_details(track_tuple)

    snippet_playback(snippet_length = snippet_length,
                     device_id = to_play_device_id,
                     track_uri = track_id,
                     sp_obj = sp_obj)
    
    if info_playback == "a":
        track_tuple = (track_data['name'], track_data['artist'])
        play_track_details(track_tuple)

    return track_data