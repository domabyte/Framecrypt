# Framecrypt

The **Encoder-Decoder Tool** is a command-line utility that allows you to encode files into a video format and decode them back to their original format. This tool is useful for hiding sensitive files within video frames and protecting them with a password.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Encoding a File](#encoding-a-file)
  - [Decoding a File](#decoding-a-file)
- [Contributing](#contributing)
- [License](#license)

## Getting Started
To get started with the Encoder-Decoder Tool, follow the instructions below.

## Prerequisites

Before using this tool, make sure you have the following prerequisites installed on your system:

- Python 3.x
- OpenCV
- Pillow (PIL)
- pyminizip
- tqdm

Run the following command to install the required dependencies from `requirements.txt`:
    ```pip install -r requirements.txt```

## Encoding a File

    1. Clone or download this repository to your local machine.

    2. Open a terminal and navigate to the project directory.

    3. Run the main.py script: ```python main.py```

    4. Select "Encode a file" (Option 1) from the menu.

    5. Enter the path to the file you want to encode when prompted.

    6. Choose a password to protect the ZIP file containing the encoded data.

    7. The tool will create a password-protected ZIP file with the encoded data and save it as locked.zip. It will also generate video frames containing the encoded data.

## Decoding a File

    1. Follow steps 1-3 from the "Encoding a File" section.

    2. Select "Decode a file" (Option 2) from the menu.

    3. Enter the name of the video file that contains the encoded data. You can press Tab to autocomplete the filename.

    4. The tool will decode the data from the video frames and save it as decoded_file.zip.

    5. Enter the password you used to protect the ZIP file during encoding.

    6. The tool will extract the original file from decoded_file.zip.