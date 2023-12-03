# Song Wrong
Pub trivia is hard and the music round is the hardest. Super quick Python single file CLI app to let you test your knowledge of various decades and genres (as defined in `playlists.json`). 

## Set Up
Usage depends on a `.env` file with the following parameters:
```
SPOTIPY_CLIENT_ID = "spotify_client_id"
SPOTIPY_CLIENT_SECRET = "spotify_client_secret"
SPOTIPY_REDIRECT_URI = "redirect_uri"
```
For local use, it's recommended to set reidrect to `http://localhost:8888/callback` for simplicity.

It's recommended to run in a `venv` to avoid dependancy issues. The following commands will set up a `venv` and install the required modules.

```
python3 -m venv song_wrong_venv
cd song_wrong_venv
source bin/activate
git clone git@github.com:colinsyyip/song_wrong.git
cd song_wrong
python3 -m pip install -r requirements.txt
```

## Usage
Sample usage for running `song_wrong` for 80s music, for 5 songs, for 20 seconds per song, using a device named `RatBook Pro`.
```
python3 song_wrong.py -p 80s -d "RatBook Pro" -n 5 -l 20
```

## Reference Docs
Help text for parameters below: 
```
 PLAYLIST: -p , --playlist, Playlist must be one of the keys in playlists.json or the word, shuffle, for a random decade each time
DEVICE: -d , --device, Device name to play on. This must be an exact string match. No value will default to the first device returned.
LENGTH: -l, --length, Length of each snippet in seconds, starting from the beginning of the song. It is not recommned for an l <= 5, due to API restrictions.
NUMBER: -n, --number, The number of songs to loop through. A value of -1 will loop indefinitely untril CTRL+C to end the program.
```