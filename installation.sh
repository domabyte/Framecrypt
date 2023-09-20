#!/bin/bash

# Function to install npm
install_npm() {
    if ! command -v npm &> /dev/null; then
        echo "npm not found. Installing npm..."
        apt-get update
        apt-get install npm -y
    else
        echo "npm is already installed. Skipping npm installation."
    fi
}

# Function to install pip
install_pip() {
    if ! command -v pip &> /dev/null; then
        echo "pip not found. Installing pip..."
        apt-get install python3-pip -y
    else
        echo "pip is already installed. Skipping pip installation."
    fi
}

create_directories() {
    if [ ! -d "encoded_videos" ]; then
        mkdir encoded_videos
    else 
        echo "encoded_videos folder already exists. Skipping ...\n"
    fi
    
    if [ ! -d "decoded_files" ]; then
        mkdir decoded_files
    else 
        echo "decoded_files folder already exists. Skipping ...\n"
    fi

}

install_python_requirements() {
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Skipping Python requirements installation.\n"
    fi
}

install_npm_packages() {
    if [ -f "Youtube-Upload/package.json" ]; then
        cd Youtube-Upload
        npm install
        cd ..
    else
        echo "package.json not found. Skipping npm package installation.\n"
    fi
}

install_mpg123() {
    apt-get install -y mpg123
}
GREEN="\e[32m"
BLUE="\e[36m"
RESET="\e[0m"

echo "${BLUE}Installing npm packages...${RESET}"
install_npm

echo "\n${BLUE}Installing pip...${RESET}"
install_pip

echo "\n${BLUE}Creating required directories...${RESET}"
create_directories

echo "\n${BLUE}Installing Python requirements..${RESET}."
install_python_requirements

echo "\n${BLUE}Installing mpg123...${RESET}"
install_mpg123

echo "\n\n${GREEN}Installation completed. Happy Encoding!! 😶${RESET}"