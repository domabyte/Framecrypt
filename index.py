import os
import cv2
import time
from PIL import Image, ImageDraw
import pyminizip
import zipfile
from tqdm import tqdm

def prompt_user(prompt, validator):
    while True:
        try:
            user_input = input(prompt).strip("'\"")
            if validator(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            print("User interrupted the process.")
            raise Exception("Thanks for using this tool!")

def create_password_protected_zip(input_file, password):
    try:
        pyminizip.compress(input_file, None, "locked.zip", password, 5)
        print("Password-protected ZIP file successfully created!")
        encode_to_frames("locked.zip")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def extract_password_protected_zip(zip_file_name, password):
    try:
        with zipfile.ZipFile(zip_file_name, "r") as zip_file:
            zip_file.extractall(pwd=password.encode())
        print("Password-protected ZIP file successfully extracted!")
        os.remove(zip_file_name)
    except zipfile.BadZipFile as e:
        print(f"Error: The ZIP file is corrupted or not in the correct format: {str(e)}")
    except RuntimeError as e:
        print(f"Error: Incorrect password or unable to decrypt the ZIP file: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def encode_to_frames(input_file):
    # Check if the encoded file exists
    output_file_name = "encoded_video"
    file_num = 1
    if os.path.exists(f"{output_file_name}.mp4") is False:
        pass
    else:
        while os.path.exists(f"{output_file_name}({file_num}).mp4"):
            file_num += 1
        output_file_name = f"{output_file_name}({file_num})"

    # Define Video Size
    video_width = 1280
    video_height = 720

    # Define Pixel Density
    pixel_density = 8

    # Define Remaining Variables
    current_x = 0
    current_y = 0
    frame_count = 0
    video = cv2.VideoWriter(
        f"{output_file_name}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (video_width, video_height)
    )
    img = Image.new("1", (video_width, video_height), "black")
    print("Generating frames, please wait...")

    # Generate Density Info Frame
    if len(str(pixel_density)) == 1:
        density_binary = "".join(format(byte, "08b") for byte in str(0).encode("utf-8"))
        for a in range(len(density_binary)):
            if density_binary[a] == "1":
                ImageDraw.Draw(img).rectangle(
                    (current_x, current_y, current_x + (video_width / 8) - 1, current_y + (video_height / 2) - 1),
                    fill="white", outline=None, width=1
                )
            current_x += video_width / 8
        current_x = 0
        current_y += video_height / 2

    for a in range(len(str(pixel_density))):
        density_binary = "".join(
            format(byte, "08b") for byte in str(pixel_density)[a].encode("utf-8")
        )
        for b in range(len(density_binary)):
            if str(density_binary)[b] == "1":
                ImageDraw.Draw(img).rectangle(
                    (current_x, current_y, current_x + (video_width / 8) - 1, current_y + (video_height / 2) - 1),
                    fill="white", outline=None, width=1
                )
            current_x += video_width / 8
        current_x = 0
        current_y += video_height / 2

    img.save("cache.png")
    video.write(cv2.imread("cache.png"))
    img = Image.new("1", (video_width, video_height), "black")
    frame_count += 1
    current_x = 0
    current_y = 0

    # Generate and Write Frames
    tic = time.perf_counter()
    with open(input_file, "rb") as f:
        byte_count = os.path.getsize(input_file)
        with tqdm(total=byte_count, unit="byte", unit_scale=True) as progress_bar:
            while byte := f.read(1):
                binary = "{0:08b}".format(int(hex(byte[0])[2:], 16))
                for a in range(len(binary)):
                    if binary[a] == "1":
                        ImageDraw.Draw(img).rectangle(
                            (current_x, current_y, current_x + pixel_density - 1, current_y + pixel_density - 1),
                            fill="white", outline=None, width=1
                        )
                    current_x += pixel_density
                    if current_x > video_width - 1:
                        current_x = 0
                        current_y += pixel_density
                        if current_y > video_height - 1:
                            current_x = 0
                            current_y = 0
                            img.save("cache.png")
                            video.write(cv2.imread("cache.png"))
                            img = Image.new("1", (video_width, video_height), "black")
                            frame_count += 1
                progress_bar.update(1)  # Update the progress bar

        img.save("cache.png")
        video.write(cv2.imread("cache.png"))
        toc = time.perf_counter()
        os.remove("cache.png")
        video.release()
        frame_count += 1
    print(f"Generated {frame_count} frames in {toc - tic:0.4f} seconds.")
    cv2.destroyAllWindows()
    os.remove(input_file)

def decode_frames(input_file):
    while not os.path.isfile(input_file):
        print("Oops! File does not exist.")
        input_file = input("Enter the file to decode: ")
    cap = cv2.VideoCapture(input_file)

    output_file = "decoded_file.zip"

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
    density = int(
        bytes(int(binary[i : i + 8], 2) for i in range(0, len(binary), 8)).decode("utf-8")
    )
    binary = ""

    # Read and Decode Frames
    with open(output_file, "wb") as file:
        for a in tqdm(range(frames - 1), unit=" FP"):
            cap.set(1, a + 1)
            res, frame = cap.read()
            cv2.imwrite("cache.png", frame)
            image = Image.open("cache.png")
            for b in range(int(height / density)):
                for c in range(int(width / density / 8)):
                    for i in range(8):
                        coordinate = (c * 8 * density) + (
                            i * density
                        ) + 2, b * density + 2
                        color = image.getpixel(coordinate)
                        if color[0] > 128:
                            binary += "1"
                        elif color[0] < 128:
                            binary += "0"
                    if len(hex(int(binary, 2))) > 3:
                        file.write(bytearray.fromhex(hex(int(binary, 2))[2:]))
                    elif len(hex(int(binary, 2))) == 3:
                        file.write(
                            bytearray.fromhex(hex(int(binary, 2)).replace("0x", "0"))
                        )
                    binary = ""
    os.remove("cache.png")
    file.close()
    print("Decoding completed successfully.")
    os.remove(input_file)
    password = str(input("Enter the password to extract: "))
    extract_password_protected_zip(output_file, password)

def main():
    print("What would you like to do?")
    print("[1] Encode a file")
    print("[2] Decode a file")

    user_choice = prompt_user("Enter your choice (1/2): ", lambda x: x in ["1", "2"])

    if user_choice == "1":
        input_file = prompt_user("Enter the file to encode: ", os.path.isfile)
        password = input("Enter a password to protect the ZIP file: ")
        create_password_protected_zip(input_file, password)
    elif user_choice == "2":
        input_file = prompt_user(
            "Enter the file to decode (e.g., encoded_file.mp4): ", os.path.isfile
        )
        decode_frames(input_file)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()