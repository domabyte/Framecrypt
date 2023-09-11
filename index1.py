import os
import cv2
import time
from PIL import Image, ImageDraw
import pyminizip
import zipfile

def error_handling(prompt, validator):
    while True:
        try:
            user_input = input(prompt)
            if validator(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            print("Oops! Strong keyboard stroke detected.")
            raise Exception("Thanks for using this tool!")

def create_password_protected_zip(file_name, password):
    try:
        file_name_without_extension, _ = os.path.splitext(os.path.basename(file_name))
        pyminizip.compress(file_name, None, f'{file_name_without_extension}.zip', password, 5)
        print("Password-protected ZIP file created successfully!")
    except Exception as e:
        print(f'An error occurred: {str(e)}')

def extract_password_protected_zip(zip_file_name, password):
    try:
        with zipfile.ZipFile(zip_file_name, 'r') as zip_file:
            zip_file.extractall(pwd=password.encode())
        print("Password-protected ZIP file extracted successfully!")
    except zipfile.BadZipFile as e:
        print(f'Error: The ZIP file is corrupted or not in the correct format: {str(e)}')
    except RuntimeError as e:
        print(f'Error: Incorrect password or unable to decrypt the ZIP file: {str(e)}')
    except Exception as e:
        print(f'An error occurred: {str(e)}')

def encode_to_frames(input_file):
    # Rest of the code for encoding to frames
    input_file = input("What file should I encode? (i.e input.zip): ")
    while not os.path.isfile(input_file):
        print("Oops! File does not exist.")
        input_file = input("What file should I encode?: ")

    # Checking if encoded file exists
    file_name = "Infinity-Drive"
    file_num = 1
    if os.path.exists(f"{file_name}.mp4") is False:
        pass
    else:
        while os.path.exists(f"{file_name}({file_num}).mp4"):
            file_num += 1
        file_name = f"{file_name}({file_num})"

    # Define Video Size
    width = 1280
    height = 720

    # Define Pixel Density
    density = 8

    # Define Remaining Variables
    w_pix = 0
    h_pix = 0
    frames = 0
    video = cv2.VideoWriter(f"{file_name}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
    img = Image.new('1', (width, height), "black")
    print("Generating frames, please be patient...")

    # Generate Density Info Frame
    if len(str(density)) == 1:
        density_binary = "".join(format(byte, '08b') for byte in str(0).encode('utf-8'))
        for a in range(len(density_binary)):
            if density_binary[a] == "1":
                ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + (width / 8) - 1, h_pix + (height / 2) - 1), fill="white", outline=None, width=1)
            w_pix += (width / 8)
        w_pix = 0
        h_pix += (height / 2)
    for a in range(len(str(density))):
        density_binary = "".join(format(byte, '08b') for byte in str(density)[a].encode('utf-8'))
        for b in range(len(density_binary)):
            if str(density_binary)[b] == "1":
                ImageDraw.Draw(img).rectangle((w_pix, h_pix, w_pix + (width / 8) - 1, h_pix + (height / 2) - 1),fill="white", outline=None, width=1)
            w_pix += (width / 8)
        w_pix = 0
        h_pix += (height / 2)
    img.save("cache.png")
    video.write(cv2.imread("cache.png"))
    img = Image.new('1', (width, height), "black")
    frames += 1
    w_pix = 0
    h_pix = 0

    # Generate and Write Frames
    tic = time.perf_counter()
    with open(input_file, "rb") as f:
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
        os.remove("cache.png")
        video.release()
        frames += 1
    print("Generated " + str(frames) + f" frames in {toc - tic:0.4f} seconds.")
    cv2.destroyAllWindows()


def decode_frames(input_file, output_file):
    # Rest of the code for decoding from frames
    while not os.path.isfile(input_file):
        print("Oops! File does not exist.")
        input_file = input("What file should I decode?: ")
    cap = cv2.VideoCapture(input_file)

    while os.path.exists(output_file):
        print("Oops! File already exists.")
        output_file = input("What should I name the output file?: ")

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

def main():
    print("What would you like to do?")
    print("[1] ENCODE a file")
    print("[2] DECODE a file")

    user_choice = error_handling("Enter your choice (1/2): ", lambda x: x in ["1", "2"])

    if user_choice == "1":
        input_file = error_handling("Enter the file to encode: ", os.path.isfile)
        password = input("Enter a password to protect the ZIP file: ")
        create_password_protected_zip(input_file, password)
        encode_to_frames(input_file)
    elif user_choice == "2":
        input_file = error_handling("Enter the file to decode: ", os.path.isfile)
        output_file = error_handling("Enter the output file name: ", lambda x: not os.path.exists(x))
        decode_frames(input_file, output_file)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
