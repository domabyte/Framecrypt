import os
import pyminizip
import zipfile
import cv2
from PIL import Image, ImageDraw

#global errorhandling program
def errorHandling(param1,param2):
        try:
            valid_inp = int(input("\nEnter your choice here: "))
            if(valid_inp > param1 and valid_inp < param2):
                return valid_inp
            else:
                 print('Enter in range of [1,2]')
        except ValueError:
            print("Error! Enter an integer value!! You fkin' dumb asshole")
        except KeyboardInterrupt:
            print("OOPs feelin' like a very strong keyboard stroke")
            raise Exception("Thanks for coming!!")


def create_passwd_protected_zip(file_name,passwd):
    # try:
    #     #Remove extension name 
    file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]

    #     # Create a password protected ZIP file
    #     pyminizip.compress(file_name,None, f'{file_name_without_extension}.zip',passwd,5)
    #     print("Password-protected ZIP file created successfully!")
    # except Exception as e:
    #     print(f'An error occurred: {str(e)}')
        
    while str(os.path.isfile(file_name)) != "True":
         print("Oops! File is missing in the current directory")
    file_size = os.path.getsize(file_name)

    #Checking if file is already encoded exists
    file_num = 1
    if os.path.exists(f'{file_name}.mp4') is False:
        pass
    else:
        while os.path.exists(f'{file_name}({file_num}).mp4'):
            file_num += 1
            file_name = f'{file_name}({file_num})'

    #Define video size or quality of the frame i.e, 720p in our case
    width = 1280
    height = 720

    # Define individual pixel density
    density = 8

    video = cv2.VideoWriter(f'{file_name_without_extension}.mp4',cv2.VideoWriter_fourcc(*'mp4v'),30,(width,height))
    img = Image.new('1', (width, height), "black")
    print("Generating frames, please be patient...")

    # Generate Density Info Frame
    if len(str(density)) == 1:
        density_binary = 

def extract_passwd_protected_zip(zip_file_name, passwd):
    try:
        with zipfile.ZipFile(zip_file_name, 'r') as zip_file:
            # Attempt to extract files with the provided password
            zip_file.extractall(pwd=passwd.encode())

        print("Password-protected ZIP file extracted successfully!")
    except zipfile.BadZipFile as e:
        print(f'Error: The ZIP file is corrupted or not in the correct format: {str(e)}')
    except RuntimeError as e:
        print(f'Error: Incorrect password or unable to decrypt the ZIP file: {str(e)}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


def encoding():
    file_name = input("Enter a file or folder name [e.g. file.txt] which you want to encode into frames: ")
    passwd = input("Enter the password to protect zip file: ")
    create_passwd_protected_zip(file_name,passwd)

def decoding():
     file_name = str(input("Enter a file or folder name [e.g. file.txt] which you want to decode: "))
     passwd = str(input("Enter the password to unzip the file: "))
     extract_passwd_protected_zip(file_name,passwd)

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