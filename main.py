from error_handling import prompt_user
from create_password_protected_zip import create_password_protected_zip
from decode_frames import decode_frames
from greeting import display_intro
import os

def main():
    display_intro()
    print("What would you like to do?")
    print("[1] Encode a file")
    print("[2] Decode a file")

    user_choice = prompt_user("Enter your choice (1/2): ", lambda x: x in ["1", "2"])

    #Handling user_choice
    if user_choice == "1":
        input_file = prompt_user("Enter the file to encode: ", os.path.isfile)
        password = input("Enter a password to protect the ZIP file: ")
        create_password_protected_zip(input_file, password)
    elif user_choice == "2":
        input_file = prompt_user("Enter the file to decode (e.g., encoded_video.mp4): ", os.path.isfile)
        decode_frames(input_file)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()