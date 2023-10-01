#!/bin/bash

main(){
    if [ $# -lt 3 ]; then
        usage
    fi
    
}

usage(){
    printf "usage: \`horcrux bind [<directory>]\` | \`horcrux [-t] [-n] split <filename>\`\n -n: number of horcruxes to make\n -t: number of horcruxes required to resurrect the original file\n example: horcrux -t 3 -n 5 split diary.txt\n"
    exit 1
}

main "$@"
