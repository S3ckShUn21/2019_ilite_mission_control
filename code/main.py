import RPi.GPIO as GPIO
import matricies as Matrix
import time
import subprocess

# Global Vars
last_button_pressed = "None"
switch_state = -1

# Time in seconds before you can press the same button again
allowed_time_between_button_presses = 3

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
    ["bellypan_pneumatics", "graphics", "website", "playbook", "electronics"],
    ["dt_intake", "elevator", "climber", "flower_cargoshooter", "3d_print"],
    ["programming", "left", "right", "hosting_comps", "team_history"]
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
led_matrix_cols_pins = [18, 22, 24, 26, 32]
# These are connected to the base of the transistor (active HIGH)
led_matrix_rows_pins = [8, 10, 12, 16]

# The button_keypad object that gets setup later
button_keypad = None

# LED Matrix object that gets setup later
LED_matrix = None

# These are functional pins that don't have media attached to them
switch_read_pin = 31
end_program_pin = 29

# Time in ms
pin_debounce_time = 42

# Functions


def button_pressed_callback(pin_name):
    global last_button_pressed, switch_read_pin, media, LED_matrix, allowed_time_between_button_presses

    # time_last_button_pressed = time.time()

    # if pin_name == "left":
    #     subprocess.call("xdotool key Left")
    # elif pin_name == "right":
    #     subprocess.call("xdotool key Right")
    # else:
    #     # You can't press the same button twice unless 'allowed time has passed'
    #     if last_button_pressed != pin_name or time.time() > time_last_button_pressed + allowed_time_between_button_presses:
    #         # Start a thread to turn on the LED of the button that was just pressed for a short time
    #         Thread(target=LED_matrix.driveLED, args=(pin_name)).start()

    #         # Read switch to determine which media to play
    #         # This will either be 0 or 1
    #         switch_state = GPIO.input(switch_read_pin)

    #         # Basically cross reference the pin number with the media file names
    #         file_name = media[pin_name][switch_state]
    #         subprocess.call("./switch_process.sh ../media/" +
    #                         file_name, shell=True)

    #         # Makes itso you cant mash the same button while its already running
    #         last_button_pressed = pin_name
    #  Thread(target=LED_matrix.driveLED, args=(pin_name)).start()
    print("Button callback says: " + pin_name)
    # LED_matrix.driveLED( pin_name )

    # TESTING:
    # Test with LED on for 10 seconds, multiple LEDs should be handled correctly,
    # though the brightness will dim as more LEDs are added
    LED_matrix.ledOn( pin_name, 10.0 )


# This creates the button_keypad and then sets up the switch read and end program
def setup_pins():
    global button_keypad, LED_matrix, switch_read_pin, end_program_pin, keypad_rows_pins, keypad_cols_pins, led_matrix_rows_pins, led_matrix_cols_pins

    # Setup the matrix that will handle the turning on the LEDs
    # LED_matrix = Matrix.LEDMatrix(
    #    keypad_vals, led_matrix_rows_pins, led_matrix_cols_pins)

    # TESTING:
    # This is to test the LED cycle matrix
    LED_matrix = Matrix.LEDMatrixCycle(
        keypad_vals, led_matrix_rows_pins, led_matrix_cols_pins)
    LED_matrix.start()

    # JMS: Moved this to after the LED Matrix is created to avoid possible race 
    # condition of button being pressed and button_pressed_callback being called
    # before the LED Matrix was created.
    # Creating the actual button_keypad
    button_keypad = Matrix.ButtonMatrix(
        keys=keypad_vals, row_pins=keypad_rows_pins, col_pins=keypad_cols_pins, callback_function=button_pressed_callback)


    # The pin the reads the switch state; it is SPDT and one way pulls low the other pulls high
    GPIO.setup(switch_read_pin, GPIO.IN)
    # The kill switch button (active HIGH)
    GPIO.setup(end_program_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print("Pin setup complete")

# Main
# This program works on callback functions whenever a button is pressed


if __name__ == "__main__":

    GPIO.cleanup()

    # Self explanitory init
    setup_pins()

    # This just has the program run until the 'END' button is pressed
    # That button will be inside the control pannel, away from prying eyes
    GPIO.wait_for_edge(end_program_pin, GPIO.RISING)

    print("Ending the Main loop")

    # TESTING:
    LED_matrix.stop()

    button_keypad.cleanupMatrix()
    GPIO.cleanup()
