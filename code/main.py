import RPi.GPIO as GPIO
from pad4pi import rpi_gpio as KEY
from threading import Thread
import time
import subprocess

# This will be the object that controls turning the lights on
# The pad4pi library can only read ; this object will drive the leds when we want
class LEDMatrix():
    def __init__(self, keys, row_pins, col_pins, gpio_mode=GPIO.BOARD):
        self._keys = keys
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._gpio_mode = gpio_mode
        self._name_index = {}

        # Searching through the array everytime is really slow
        # This creates a hashmap basically for what led row and col to turn on
        self._setupNameIndex()

        # Set the matrix pins as outputs
        self._setupPins()

    def _setupNameIndex(self):
        # Num rows
        for i in range(len(self._keys)):
            # Num cols
            for j in range(len(self._keys[0])):
                # Adds a dictionary entry with the coordinate of the value
                self._name_index[self._keys[i][j]] = (i,j)

    def _setupPins(self):
        # Setup all of the pins as outputs
        GPIO.setmode(self._gpio_mode)
        # First do the columns; they will be driven low, therefore they have a pullUP resistor
        for pin in self._col_pins:
            GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

        # Second do the rows; rows will be driven high, therefore 'normal mode' is pullDOWN
        for pin in self._row_pins:
            GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

    # Figure out the pin numbers to drive high/low
    # Turn the led on ON A DIFFERENT THREAD because it will be on for a set amount of time
    # We don't want it impeading the timer of the 
    # time on is seconds for the light to stay on
    def driveLED(self, ledName, timeOn=0.25):
        # Coordinate x y of the led name
        coord = self._name_index[ledName]
        # Cols are Y value
        col_pin = self._col_pins[coord[1]]
        # Cols are driven low
        GPIO.ouput(col_pin, GPIO.LOW)    
        row_pin = self._row_pins[coord[0]]
        # Rows are dirven high
        GPIO.output(row_pin, GPIO.HIGH)
        time.sleep(timeOn)
        # Switch LED back to off position
        GPIO.output(col_pin, GPIO.HIGH)
        GPIO.output(row_pin, GPIO.LOW)


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
    ["outreach", "build", "steam_expo", "summer_camp_vid", "vision_pathfollowing"],
    ["bellypan_pneumatics","graphics","website","playbook","electronics"],
    ["dt_intake","elevator","climber","flower_cargoshooter","3d_print"],
    ["programming","left","right","hosting_comps","team_history"]
]
# There are 4
# The library sets the columns as outputs
# I am following the schematic of Mr. Luban's for reference
keypad_cols_pins = [5, 7, 11, 13, 15]
# There are 5
# The library sets the rows as inputs
# I am following the schematic of Mr. Luban's for reference
keypad_rows_pins = [36, 37, 38, 40] 

# These are connected to the emitter of the transistor (active LOW)
led_matrix_cols_pins = [18,22,24,26,32]
# These are connected to the base of the transistor (active HIGH)
led_matrix_rows_pins = [8,10,12,16]

# The button_keypad object that gets setup later
button_keypad = None

# LED Matrix object that gets setup later
LED_matrix = None

# These are functional pins that don't have media attached to them
# TODO: Change these to the correct pin vals
switch_read_pin = 31
end_program_pin = 29

# Time in ms
pin_debounce_time = 42

# Functions
def my_callback(pin_name):
    global last_button_pressed, switch_read_pin, media, LED_matrix

    if last_button_pressed != pin_name:

        if pin_name == "left":
            subprocess.call("xdotool key Left")
        elif pin_name == "right":
            subprocess.call("xdotool key Right")
        else:
            # Start a thread to turn on the LED of the button that was just pressed for a short time
            Thread( target=LED_matrix.driveLED, args=(pin_name)).start()

            # Read switch to determine which media to play
            # This will either be 0 or 1
            switch_state = GPIO.input(switch_read_pin)

            # Basically cross reference the pin number with the media file names
            file_name = media[pin_name][switch_state]
            subprocess.call("./switch_process.sh ../media/" +
                            file_name, shell=True)

            # Makes itso you cant mash the same button while its already running
            last_button_pressed = pin_name


# This creates the button_keypad and then sets up the switch read and end program
def setup_pins():
    global button_keypad, LED_matrix
    # Creating the actual button_keypad
    button_keypad = KEY.KeypadFactory().create_keypad(
        button_keypad=keypad_vals, row_pins=keypad_rows_pins, col_pins=keypad_cols_pins, gpio_mode=GPIO.BOARD)

    # Apply the callback function to whenever any of the keys are pressed
    button_keypad.registerKeyPressHandler(my_callback)

    # Setup the matrix that will handle the turning on the LEDs 
    LED_matrix = LEDMatrix(keypad_vals, keypad_rows_pins, keypad_cols_pins)

    # TODO: setup the end_program and switch_read GPIOs

# Main
# This program works on callback functions whenever a button is pressed

if __name__ == "__main__":

    # Self explanitory init
    setup_pins()

    # This just has the program run until the 'END' button is pressed
    # That button will be inside the control pannel, away from prying eyes
    GPIO.wait_for_edge(end_program_pin, GPIO.RISING)

    print("Ending the Main loop")
