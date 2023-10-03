#!/bin/bash

# Function to check directory path
getHorcruxPathsInDir() {
    local dirpath=$1
    local paths=()

    while IFS= read -r path; do
        paths+=("$path")
        echo "$path"
    done < <(find "$dirpath" -maxdepth 1 -type f -name "*.horcrux")

    if [ ${#paths[@]} -eq 0 ]; then
        echo "No .horcrux files found in $dirpath"
        return 1
    fi
}

export -f getHorcruxPathsInDir