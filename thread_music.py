import threading
from mpyg321.MPyg123Player import MPyg123Player 
from create_password_protected_zip import create_password_protected_zip

def play_music():
    player = MPyg123Player()
    music_file = "testing_file_song.mp3"
    player.play_song(music_file)

# Function to perform encoding
def perform_encoding(input_file, password):
    # Start the music thread before encoding
    music_thread = threading.Thread(target=play_music)
    music_thread.start()
    create_password_protected_zip(input_file, password)
    # Wait for the music thread to finish
    music_thread.join()