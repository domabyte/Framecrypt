import os
import pyminizip
import zipfile
import cv2
import time
import tqdm
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
    try:
        #Remove extension name 
        file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]

        # Create a password protected ZIP file
        pyminizip.compress(file_name,None, f'{file_name_without_extension}.zip',passwd,5)
        print("Password-protected ZIP file created successfully!")
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        
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

    # Define Remaining Variables
    w_pix = 0
    h_pix = 0
    frames = 0

    video = cv2.VideoWriter(f'{file_name_without_extension}.mp4',cv2.VideoWriter_fourcc(*'mp4v'),30,(width,height))
    img = Image.new('1', (width, height), "black")
    print("Generating frames, please be patient...")
    
    # Generate and Write Frames
    tic = time.perf_counter()
    with open(file_name, "rb") as f:
        while byte := f.read(1):
            binary = "{0:08b}".format(int(hex(byte[0])[2:], 16))
            for a in range(len(binary)):
                if binary[a] == "1":
                    ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + density - 1, h_pix + density - 1),
                                                  fill="white",
                                                  outline=None, width=1)
                w_pix += density
                if w_pix > width - 1:
                    w_pix = 0
                    h_pix += density
                    if h_pix > height - 1:
                        w_pix = 0
                        h_pix = 0
                        img.save("cache.png")
                        video.write(cv2.imread("cache.png"))
                        img = Image.new('1', (width, height), "black")
                        frames += 1
        img.save("cache.png")
        video.write(cv2.imread("cache.png"))
        toc = time.perf_counter()
        # os.remove("cache.png")
        video.release()
        frames += 1
    print("Generated " + str(frames) + f" frames in {toc - tic:0.4f} seconds.")
    cv2.destroyAllWindows()

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
    while str(os.path.isfile(file_name)) != "True":
        print("Oops! File does not exist.")
        file_name = input("What file should I encode?: ")
    passwd = input("Enter the password to protect zip file: ")
    create_passwd_protected_zip(file_name,passwd)

def decoding():
     # Define Input File
    file_name = input("What file should I decode? (i.e index.mp4): ")
    while str(os.path.isfile(file_name)) != "True":
        print("Oops! File does not exist.")
        file_name = input("What file should I decode?: ")
    cap = cv2.VideoCapture(file_name)

    # Define Output File
    output_file = input("What should I name the output file? (i.e output.zip): ")
    while str(os.path.exists(output_file)) == "True":
        print("Oops! File already exists.")
        output_file = input("What should I name the output file?: ")

    # Define Variables
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(1, 0)
    res, frame = cap.read()
    cv2.imwrite("cache.png", frame)
    width = cv2.imread("cache.png", cv2.IMREAD_UNCHANGED).shape[1]
    height = cv2.imread("cache.png", cv2.IMREAD_UNCHANGED).shape[0]
    binary = ""

    # Get Density
    image = Image.open("cache.png")
    for a in range(2):
        for b in range(8):
            coordinate = (width / 8) * b + 2, (height / 2) * a + 2
            color = image.getpixel(coordinate)
            if color[0] > 128:
                binary += "1"
            elif color[0] < 128:
                binary += "0"
    density = int(bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8)).decode('utf-8'))
    binary = ""

    # Read and Decode Frames
    with open(output_file, "wb") as file:
        for a in tqdm(range(frames - 1), unit=' FP'):
            cap.set(1, a + 1)
            res, frame = cap.read()
            cv2.imwrite("cache.png", frame)
            image = Image.open("cache.png")
            for b in range(int(height / density)):
                for c in range(int(width / density / 8)):
                    for i in range(8):
                        coordinate = (c * 8 * density) + (i * density) + 2, b * density + 2
                        color = image.getpixel(coordinate)
                        if color[0] > 128:
                            binary += "1"
                        elif color[0] < 128:
                            binary += "0"
                    if len(hex(int(binary, 2))) > 3:
                        file.write(bytearray.fromhex(hex(int(binary, 2))[2:]))
                    elif len(hex(int(binary, 2))) == 3:
                        file.write(bytearray.fromhex(hex(int(binary, 2)).replace("0x", "0")))
                    binary = ""
    os.remove("cache.png")
    file.close()
    passwd = str(input("Enter password for the file : "))
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