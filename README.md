# Framecrypt

The **Encoder-Decoder Tool** is a command-line utility that allows you to encode files into a video format and decode them back to their original format. This tool is useful for hiding sensitive files within video frames and protecting them with a password and also upload the file into your youtube account.

[NOTE]: This is available for linux user only for now. Please create support for windows and macos users by contributing to this project.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
  - [Encoding a File](#encoding-a-file)
  - [Decoding a File](#decoding-a-file)
  - [Creating client secrets json](#creating-youtube-client-secrets)
  - [Uploading a File](#uploading-a-file)
  - [Fetching VideoID](#fetching-a-video)

## Getting Started
To get started with the Encoder-Decoder Tool, follow the instructions below.

## Prerequisites

Before using this tool, make sure you have the following prerequisites installed on your system:

- Python 3.x
- OpenCV
- Pillow (PIL)
- pyminizip
- tqdm
- mpyg321

Run the following command to install the required dependencies from `requirements.txt`:
    ```pip install -r requirements.txt```

## Encoding a File
  1. Clone or download this repository to your local machine.
  
  2. Open a terminal and navigate to the project directory.

  3. Run the main.py script: ```python main.py```

  4. Select "Encode a file" (Option 1) from the menu.

  5. Enter the name to the file you want to encode when prompted [Note]: Please keep files in the same directory.

  6. Choose a password to protect the ZIP file containing the encoded data.

  7. The tool will create a password-protected ZIP file with the encoded data and save it as locked.zip. It will also generate video frames containing the encoded data into encoded_videos folder and fun fact is that you could listen some of my favourite music in parallel.

## Decoding a File
  1. Follow steps 1-3 from the "Encoding a File" section.

  2. Select "Decode a file" (Option 2) from the menu.

  3. Enter the name of the video file that contains the encoded data from encoded_videos folder.

  4. The tool will decode the data from the video frames and save it as decoded_file.zip.

  5. Enter the password you used to protect the ZIP file during encoding.

  6. The tool will extract the original file from decoded_file.zip into decoded_files folder.


## Creating YOUTUBE CLIENT SECRETS
  1. To choose this option you have to use YOUTUBE v3 API from google cloud. Follow this link to login/signup into your [_Google Cloud Console_](https://console.cloud.google.com/)

  2. If you don't have a Google Cloud project, create one by clicking the project dropdown in the upper left corner and selecting "New Project." Give your project a name and click "Create."

  3. In the left sidebar, click on "APIs & Services" and add ```+ ENABLE APIS AND SERVICES```.

  4. Search for YOUTUBE V3 API or similar and Enable it.

  5. Now go to "Credentials" in left sidebar and click on ```+ CREATE CREDENTIALS``` and select ```OAuth client ID```.

  6. Choose "Web application" as the application type. Keep name as Web client or choose as suits you.

  7. Add URL ```http://localhost:8080``` into Authorized redirect URIs and hit Create Button and DOWNLOAD JSON.

  8. Paste this JSON in Youtube-Upload subfolder and this json to ```client_secrets.json```.

  9. Now go to ```OAuth consent screen``` in google cloud and add Test Users.
  
    [NOTE]: Only Tests users gmail can signin to youtube v3 api.

  
## Uploading a file
  [NOTE]: Make sure you follow this steps to create client_secrets.json file [#creating YOUTUBE CLIENT SECRETS](creating-youtube-client-secrets)
    
  1. Follow steps 1-3 from the "Encoding a File" section.

  2. Select "Upload the file to youtube" (Option 3) from the menu.

  3. Enter the name of the file from encoded_videos folder that contains the videos.

  4. Enter required data into field such as title, description and then it will automatically start uploading a video into your youtube account.

  5. Now for the first time, it will ask you to follow a link

  6. Follow the link and signin only with the respective tests users gmail and allow all permissions.

  7. Then the server will refuse to connect but you will get your code in url. Copy the code starting after ```code=``` and finish before ```&```.

  8. Paste this code into your terminal and you will sucessfully sign in.

  9. Uploading will start.

    [Note]: It will keep your video as private because youtube terms of services.


## Fetching a video
  1. Follow steps 1-3 from the "Encoding a File" section.

  2. Select "To list the uploading videos of your channel" (Option 4) from the menu.

  3. You will see all the videos that you have uploaded from the authorised channel with videoID.

    [NOTE]: If installing requirements.txt leads to any error then please try this script into linux environment and install manually.
   
                                                                                             ~Dikshit singh