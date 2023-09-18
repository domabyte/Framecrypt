import subprocess

def download_yt_video():
   try:
      subprocess.run(["node","./Youtube-Upload/youtube_auth.js", "download"], check=True)
   except subprocess.CalledProcessError as e:
      print(f'Error download the video : {e}') 