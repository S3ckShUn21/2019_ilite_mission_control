#!/bin/bash
# This script kills the running slideshow or video
# Then will start the next item depending on arguments given

# Exit 0    : No issues

source ./constants.conf

# ---------
# Functions
# ---------

# Kill the running video or current slideshow
# grep returns a 0 if there is a match found
kill_the_things () {
    running_processes = ps -e

    $running_processes | grep vlc
    vlc_running = $?
    $running_processes | grep gpicview
    gpic_running = $?

    if [ vlc_running == 0 ]
    then
        echo "Killing all vlc"
        killall vlc
    elif [ gpic_running == 0 ]
    then
        echo "Killing all gpicview"
        killall gpicview
    fi
}

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
    kill_the_things
    vlc -f --no-video-title-show --mouse-hide-timeout 0 $OPTARG &
    exit 0
else
    echo "Slideshow starting"
    kill_the_things 
    # open the image
    gpicview $OPTARG
    # make full screen
    xdotool key F11
    # zoom to the correct level
    xdotool type "+++++"
    exit 0
fi
