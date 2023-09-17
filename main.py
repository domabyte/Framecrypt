from error_handling import prompt_user
from thread_music import perform_encoding,perform_decoding,perform_uploading
from decode_frames import decode_frames
from greeting import display_intro
from upload import upload_video_to_youtube
import os

def main():
    display_intro()
    print("What would you like to do?")
    print("[1] Encode a file")
    print("[2] Decode a file")
    print("[3] Upload the file to youtube")

    user_choice = prompt_user("Enter your choice (1/2/3): ", lambda x: x in ["1", "2","3"])

    #Handling user_choice
    if user_choice == "1":
        input_file = prompt_user("Enter the file to encode: ", os.path.isfile)
        password = input("Enter a password to protect the ZIP file: ")
        perform_encoding(input_file,password)

    elif user_choice == "2":
        input_file = prompt_user("Enter the file to decode (e.g., encoded_video.mp4): ", os.path.isfile)
        perform_decoding(input_file)

    elif user_choice == "3":
        perform_uploading()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
