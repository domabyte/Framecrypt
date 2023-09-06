#global errorhandling program
def errorHandling(param1,param2):
        try:
            valid_inp = int(input("\nEnter your choice here: "))
            if(valid_inp > param1 and valid_inp < param2):
                return valid_inp
            else:
                 print('Enter in range of [1,2]')
        except ValueError:
            print("Error! Enter an integer value!! You fkin' dump asshole")
        except KeyboardInterrupt:
            print("OOPs feelin' like a very strong keyboard stroke")
            raise Exception("Thanks for coming!!")

def encoding():
     print("ENCODING DONE!!")

def decoding():
     print("DECODING DONE!!")

def __main__():
    #Asking for input
    print(f'What would you like to do?\n\t[1] ENCODING the file\n\t[2] DECODING the video')

    #Validating input
    user_choice = errorHandling(0,3)

    #switch case as per response
    match user_choice:
         
         #It will call the encoding function
         case 1:
              encoding()
         case 2:
              decoding()
         case _:
              print("Encounter Error, Run again!!")

if __name__ == "__main__":
    __main__()











import os
import zipfile

def create_password_protected_zip(directory, password):
    # Iterate over all files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Create a zip file with the same name as the original file
            zip_filename = f"{file_path}.zip"
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Set a password for the zip file
                zipf.setpassword(password.encode())
                # Add the file to the zip file
                zipf.write(file_path, os.path.basename(file_path))

    print(f"All files in {directory} have been converted to password-protected zip files.")

# Example usage
create_password_protected_zip("path/to/directory", "password123")
