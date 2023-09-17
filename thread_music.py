import threading
from mpyg321.MPyg123Player import MPyg123Player
from decode_frames import decode_frames
from create_password_protected_zip import create_password_protected_zip
from upload import upload_video_to_youtube

def play_music(song_name):
    player = MPyg123Player()
    music_file = song_name
    player.play_song(music_file)

# Function to perform encoding
def perform_encoding(input_file, password):
    # Start the music thread before encoding
    music_thread = threading.Thread(target=play_music('./songs/Neil Sedaka - Oh! Carol.mp3'))
    music_thread.start()
    create_password_protected_zip(input_file, password)
    # Wait for the music thread to finish
    music_thread.join()

# Function to perform decoding
def perform_decoding(input_file):
    # Start the music thread before decoding
    music_thread = threading.Thread(target=play_music('./songs/In the still of the night.mp3'))
    music_thread.start()
    decode_frames(input_file)
    # Wait for the music thread to finish
    music_thread.join()

def perform_uploading():
    music_thread = threading.Thread(target=play_music("./songs/Engelbert Humperdinck - Can't Take My Eyes Off You.mp3"))
    music_thread.start()
    upload_video_to_youtube()
    music_thread.join()