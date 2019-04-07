#!/bin/bash
# This script kills the running slideshow or video
# Then will start the next item depending on arguments given

# Exit 0    : No issues

source ./constants.conf

# ---------
# Functions
# --------- 

# Grab the file extension of the given file to then decide which command to use
# If there is no file extension (meaning it is a folder) then cut returns the
# the whole file name -> which will never equal mp4
is_mp4 () {
    local extension="$1" | cut -d '.' -f2
    echo "File is... $1"
    echo "Extension is... $extension"
    if [ $extension == "mp4" ]
    then
        echo "Is MP4"
        return 1
    else
        echo "Not an MP4"
        return 0
    fi
}

# -----------------------
# MAIN BODY OF THE SCRIPT
# -----------------------
if [ $# -le 0 ]
then
    echo "You need to specify a file"
    exit -1
fi

is_mp4

if [ is_mp4 "$1" ]
then
    echo "Video Starting"
    killall vlc gpicview
    vlc -f --no-video-title-show --mouse-hide-timeout 0 --play-and-exit $OPTARG &
    exit 0
else
    echo "Slideshow starting"
    killall vlc gpicview
    # open the image folder
    gpicview $OPTARG
    # make full screen
    xdotool key F11
    # zoom to the correct level
    xdotool type "+++++"
    exit 0
fi
