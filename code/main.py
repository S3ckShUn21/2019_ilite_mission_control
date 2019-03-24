import RPi.GPIO as GPIO
import time
import subprocess

# Global Vars
last_button_pressed = -1
switch_state = -1

# Dictionary of all of the media filenames
media = {
    "outreach": ["outreach.pdf", "outreach.mp4"],
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

# Mapping of physical pin number to its media name
pin_vals = {
    3: "outreach",
    5: "build",
    7: "graphics",
    8: "website",
    10: "electronics",
    11: "programming",
    12: "playbook",
    15: "3d_print",
    16: "steam_expo",
    18: "summer_camp_vid",
    23: "dt_intake",
    24: "vision_pathfollowing",
    26: "bellypan_pneumatics",
    29: "elevator",
    31: "climber",
    32: "flower_cargoshooter",
    33: "hosting_comps",
    35: "team_history",
}

# These are functional pins that don't have media attached to them
left_pin = 19
right_pin = 21
end_program = 22
switch_read_pin = 36

# Time in ms
pin_debounce_time = 42
# Time in s
# Time between when different buttons can be pressed
multi_button_delay = 5


# Functions

def my_callback(channel):
    global last_button_pressed, switch_read_pin, pin_vals, media

    if last_button_pressed != channel:

        if channel == left_pin:
            subprocess.call("xdotool key Left")
        elif channel == right_pin:
            subprocess.call("xdotool key Right")
        else:

            # Read switch to determine which media to play
            # This will either be 0 or 1
            switch_state = GPIO.input(switch_read_pin)

            # Basically cross reference the pin number with the media file names
            file_name = media[pin_vals[channel]][switch_state]
            subprocess.call("./switch_process.sh ../media/" +
                            file_name, shell=True)

            # Makes itso you cant mash the same button while its already running
            last_button_pressed = channel

            # Wait for a while so the buttons can't be mashed
            time.sleep(multi_button_delay)


def setup_pins():
    global pin_vals, pin_debounce_time, left_pin, right_pin, end_program
    global switch_read_pin

    # Set up the GPIO pin numbering system
    # BOARD is the position on the board
    # BCM is the numbering of the GPIO
    GPIO.setmode(GPIO.BOARD)

    # Loop through all of the values in the pins dictionary
    # Set them up as inputs
    # Add the callback to the pins to trigger an event
    for pin_num in pin_vals.keys():
        GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin_num, GPIO.RISING, callback=my_callback,
                              bouncetime=pin_debounce_time)
        print("Setup " + pin_vals[pin_num] + " pin")
    # Now setup all of the control pins (l,r,end,switch)
    GPIO.setup(left_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(left_pin, GPIO.RISING,
                          callback=my_callback, bouncetime=pin_debounce_time)
    GPIO.setup(right_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(right_pin, GPIO.RISING,
                          callback=my_callback, bouncetime=pin_debounce_time)

    # The switch that tells which media to use
    # No callback needed, just a passive read pin
    GPIO.setup(switch_read_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # End Program pin
    # No callback required
    GPIO.setup(end_program, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print('Pin setup complete')
    # Pause and let the computer catch up
    # Number in seconds
    time.sleep(0.5)


# Main
# This program works on callback functions whenever a button is pressed

if __name__ == "__main__":

    # Self explanitory init
    setup_pins()

    # This just has the program run until the 'END' button is pressed
    # That button will be inside the control pannel, away from prying eyes
    GPIO.wait_for_edge(end_program, GPIO.RISING)

    print("Ending the Main loop")
