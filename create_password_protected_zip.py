import pyminizip
from encode_to_frames import encode_to_frames

# Creating zip file
def create_password_protected_zip(input_file, password):
    try:
        pyminizip.compress(input_file, None, "locked.zip", password, 5)
        print("Password-protected ZIP file successfully created!")
        encode_to_frames("locked.zip")
    except Exception as e:
        print(f"An error occurred: {str(e)}")