#!/bin/bash

source ./commands/bind.sh

main(){
    if [ $# -lt 2 ]; then
        usage
    fi

    if [ $1 == "bind" ]; then
        directory_path=""
        if [ $# -eq 1 ]; then
            directory_path="."
        else
            directory_path=$2
        fi
        echo "Directory path is : "$directory_path

         getHorcruxPathsInDir "$directory_path"
    else 
        echo "Invalid command: $1"
        usage
    fi

}

usage(){
    printf "usage: \`horcrux bind [<directory>]\` | \`horcrux [-t] [-n] split <filename>\`\n -n: number of horcruxes to make\n -t: number of horcruxes required to resurrect the original file\n example: horcrux -t 3 -n 5 split diary.txt\n"
    exit 1
}

main "$@"
