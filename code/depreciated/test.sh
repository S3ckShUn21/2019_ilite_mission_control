#!/bin/bash

# Turn off the screen for a moment
# xset -display :0 dpms force off

# Instead of turning off the monitor I show the screen cap for a certain amount of time
# python show_screen_saver.py 6 final.png &

# Kill the running process of vlc
ps -e | grep vlc
lastOutput=$?
echo "Last ouput : $lastOutput"	
if [ $lastOutput -ne 1 ]
then
	echo "killing vlc"
	killall vlc 	# This should work just as well as the more complicated one below
							# kill $(ps -e | grep vlc | cut -f1 -d' ')
fi
	
# Pick the next video to open up into full screen

vlc -f --no-video-title-show --mouse-hide-timeout 0 $1 &

# Turn the screen back on again after the video loads back up

#sleep 2.5

#xset -display :0 dpms force on
