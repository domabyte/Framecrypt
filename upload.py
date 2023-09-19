import subprocess

def upload_video_to_youtube():
    try:
        videoName = str(input("Enter the video name i.e, encoded_video.mp4 : "))
        title = str(input("Enter the title of the video : "))
        description = str(input("Enter the description of the video : "))
        subprocess.run(["node","./Youtube-Upload/youtube_auth.js",videoName,title,description], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error uploading video: {e}')