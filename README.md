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
* Because python is so slow compared to pure bash, I try as much as possible to run processes in shell scripts
* The ILITE_Comm...notes are sporadic random additions that may or may not be kept around
* The depreciated folder will probably be deleted soon, now that I'm using Git
* The Outreach powerpoint and related folders are there to show what the difference is in the naming scheme
    * The one that would be used is the "renammed" one
    * There won't actually be two folers in production; just the one with the same exact name as the powerpoint

## Linux Dependencies
* python3
    * tkinter : a window creation python library used to display the ilite logo
* The default image viewer for raspberry pi
* xdotool : a terminal program to simulate key strokes
    * This is used for left and right during the slide show
* VLC media player for the videos