from api import playlist_id_retrieve, spotify_login, play_random_snippet_pl
from argparse import ArgumentParser
import json
import random

parser = ArgumentParser(prog = 'Song Wrong',
                        description = "Get better at recognizing songs. You'll probably be wrong")

parser.add_argument("-p", "--playlist", 
                    required = True,
                    help = "Playlist must be one of the keys in playlists.json or the word, shuffle, for a random decade each time")
parser.add_argument("-d", "--device",
                    default = None,
                    help = "Device name to play on. This must be an exact string match. No value will default to the first device returned.")
parser.add_argument("-l", "--length",
                    default = 20,
                    help = "Length of each snippet in seconds, starting from the beginning of the song. It is not recommned for an l <= 5, due to API restrictions.")
parser.add_argument("-n", "--number", 
                    default = 1,
                    help = "The number of songs to loop through. A value of -1 will loop indefinitely untril CTRL+C to end the program.")

args = parser.parse_args()

spotify_obj = spotify_login()
playlist = args.playlist

if playlist == "shuffle":
    f = open("playlists.json")
    pl_file = json.load(f)
    pl_keys = pl_file.keys()
    pl_data = "shuffle"
else:
    pl_link = playlist_id_retrieve(playlist)
    pl_data = spotify_obj.playlist(pl_link)

length = int(args.length)
number = int(args.number)
device = args.device

if number == -1:
    while True:
        if playlist == "shuffle":
            pl_key = random.choice(pl_keys)
            pl_link = playlist_id_retrieve(pl_key)
            pl_data = spotify_obj.playlist(pl_link)
        track_info = play_random_snippet_pl(pl_data, sp_obj = spotify_obj,
                                            snippet_length = length,
                                            to_play_device = device)
        track_info_tuple = (track_info['name'], track_info['artist'])
        print("Track Name: %s \t Artist: %s" % track_info_tuple)
else:
    i = 0
    while i < number:
        if playlist == "shuffle":
            pl_key = random.choice(pl_keys)
            pl_link = playlist_id_retrieve(pl_key)
            pl_data = spotify_obj.playlist(pl_link)
        track_info = play_random_snippet_pl(pl_data, sp_obj = spotify_obj,
                                            snippet_length = length,
                                            to_play_device = device)
        track_info_tuple = (track_info['name'], track_info['artist'])
        print("Track Name: %s \t Artist: %s" % track_info_tuple)
        i += 1