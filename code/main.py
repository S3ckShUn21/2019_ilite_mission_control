import RPi.GPIO as GPIO
from pad4pi import rpi_gpio as KEY
import time
import subprocess

# Global Vars
last_button_pressed = "None"
switch_state = -1

# Dictionary of all of the media filenames or folder names
media = {
    "outreach": ["Outreach 2019 V7 Renammed", "outreach.mp4"],
    "build": ["build", "build"],
    "graphics": ["graphics", "graphics"],
    "website": ["website", "website"],
    "electronics": ["electronics", "electronics"],
    "programming": ["programming", "programming"],
    "playbook": ["playbook", "playbook"],
    "3d_print": ["3d_print", "3d_print"],
    "steam_expo": ["3d_print", "3d_print"],
    "summer_camp_vid": ["summer", "summer"],
    "dt_intake": ["dt", "dt"],
    "vision_pathfollowing": ["vision", "vision"],
    "bellypan_pneumatics": ["bp", "bp"],
    "elevator": ["elevator", "elevator"],
    "climber": ["climber", "climber"],
    "flower_cargoshooter": ["flower", "flower"],
    "hosting_comps": ["hosting", "hosting"],
    "team_history": ["history", "history"]
}

# These are the values that will output to the callback function whenever the buttons are pressed
keypad_vals = [
    ["outreach", "build", "3d_print", "programming"],
    ["graphics", "website", "playbook", "electronics"],
    ["steam_expo", "summer_camp_vid", "left", "right"],
    ["vision_pathfollowing", "bellypan_pneumatics", "hosting_comps", "team_history"],
    ["dt_intake", "elevator", "climber", "flower_cargoshooter"]
]
# There are 4
# The library sets the columns as outputs
# I am following the schematic of Mr. Luban's for reference
keypad_cols_pins = [36, 37, 38, 40]
# There are 5
# The library sets the rows as inputs
# I am following the schematic of Mr. Luban's for reference
keypad_rows_pins = [5, 7, 11, 13, 15]

# An object the library needs to create other keypads
keypad_creator = KEY.KeypadFactory()

# These are functional pins that don't have media attached to them

# Time in ms
pin_debounce_time = 42

# Functions
def my_callback(pin_name):
    global last_button_pressed, switch_read_pin, media

    if last_button_pressed != pin_name:

        if pin_name == "left":
            subprocess.call("xdotool key Left")
        elif pin_name == "right":
            subprocess.call("xdotool key Right")
        else:

            # Read switch to determine which media to play
            # This will either be 0 or 1
            switch_state = GPIO.input(switch_read_pin)

            # Basically cross reference the pin number with the media file names
            file_name = media[pin_name][switch_state]
            subprocess.call("./switch_process.sh ../media/" +
                            file_name, shell=True)

            # Makes itso you cant mash the same button while its already running
            last_button_pressed = pin_name


# This creates the keypad and then sets up the switch read and end program
def setup_pins():
    # Creating the actual keypad
    keypad = keypad_creator.create_keypad(
        keypad=keypad_vals, row_pins=keypad_rows_pins, col_pins=keypad_cols_pins, gpio_mode=GPIO.BOARD)

    # Apply the callback function to whenever any of the keys are pressed
    keypad.registerKeyPressHandler(my_callback)

# Main
# This program works on callback functions whenever a button is pressed

if __name__ == "__main__":

    # Self explanitory init
    setup_pins()

    # This just has the program run until the 'END' button is pressed
    # That button will be inside the control pannel, away from prying eyes
    GPIO.wait_for_edge(end_program, GPIO.RISING)

    print("Ending the Main loop")
