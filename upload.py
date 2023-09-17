import subprocess

def upload_video_to_youtube():
    try:
        title = str(input("Enter the title of the video : "))
        description = str(input("Enter the description of the video : "))
        tags = str(input("Enter tags (comma-separated i.e, boring,pakau) : "))
        subprocess.run(["node","./Youtube-Upload/youtube_auth.js",title,description,tags], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Error uploading video: {e}')