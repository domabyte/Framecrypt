import os
import cv2
import time
from PIL import Image, ImageDraw
from tqdm import tqdm
import shutil

def encode_to_frames(input_file):
    output_directory = "encoded_videos"

    # Check if the output directory exists, create it if not
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    output_file_name = "encoded_video"
    output_file_path = os.path.join(output_directory,"encoded_video")
    file_num = 1

   # Check if the encoded file exists
    if os.path.exists(f"{output_file_path}.mp4") is False:
        pass
    else:
        while os.path.exists(f"{output_file_path}({file_num}).mp4"):
            file_num += 1
        output_file_name = f"{output_file_name}({file_num})"

    # Define Video Size for 720p [choose this by keeping youtube compression in mind]
    video_width = 1280
    video_height = 720

    # Define Pixel Density
    pixel_density = 8

    # Define Pixel width + height as per top_left and bottom_right
    current_x = 0
    current_y = 0
    frame_count = 0
    video = cv2.VideoWriter(f'{output_file_name}.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30, (video_width, video_height))
    img = Image.new("1", (video_width, video_height), "black")
    print("Generating frames, please wait...")

    # Density info frame
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
    try:
        shutil.move(f'{output_file_name}.mp4', output_directory)
        print(f"File '{output_file_name}' moved to '{output_directory}'")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    encode_to_frames("locked.zip")