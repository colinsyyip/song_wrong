from gtts import gTTS
from pygame import mixer
import os
import time


def play_track_details(track_info_tuple, file_name = "tmp.mp3", file_path = "tmp"):
    """
    Plays track name and artist using TTS.
    """
    per_char_read_constant_s = 0.2

    if file_path not in os.listdir():
        os.makedirs("tmp")
    full_file_name = "/".join((file_path, file_name))
    track_info_cat = ", ".join(track_info_tuple)
    track_info_n_char = len(track_info_cat)
    wait_time = per_char_read_constant_s * track_info_n_char
    tts = gTTS(track_info_cat, lang='en')
    tts.save(full_file_name)

    mixer.init()
    mixer.music.load(full_file_name, "mp3")
    mixer.music.play()

    time.sleep(wait_time)

    os.remove(full_file_name)