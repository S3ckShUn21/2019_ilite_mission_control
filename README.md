# Basic Overview
There are roughly 20 buttons on the mission control panel. Each of which has a specific topic related to them. For example, one will be about outreach, another strategy, another our climber mechanism, etc.

The goal is to show videos, pictures, information, or slide shows about the specific topic when that button is pressed.

There is also a simple toggle switch on the board. Dependant upon the state of the toggle switch (1 or 0) the button pressed will have a different function. For example, pressing the outreach button with switch state 1 will show a video of outreach events we do, while pressing the outreach button again with switch state 0 will allow you to scroll through the outreach booklet (on the screen) with left and right buttons.

All 'media buttons' (not the left, right, or reset buttons) will have two sets of media 'attached' to them

## Startup
To start the whole project off I use the shell command
```
./start_command_console.sh
```
 in the code subdirectory. From there it is fairly easy to track through the process of events.

## Other Info
* Most, if not all files have a description at the top of the file for more information
* The wpa_supplicant is just a file to add into the boot partition to get the Pi to auto connect to wifi without needing a mouse or keyboard - not needed for normal operations
* The ILITE_Comm...notes are sporadic random additions that may or may not be kept around
* The depreciated folder will probably be deleted soon, now that I'm using Git

## Linux Dependencies
* xdotool : a terminal program to simulate key strokes
    * This is used for left and right during the slide show
* VLC media player for the videos