import RPi.GPIO as GPIO
import time
import subprocess

last_pin_clicked = -1
videos_dictionary = {
    15:	'dog_1',
    16:	'dog_2',
    7:	'dog_3',
    8:	'temp',
    10:	'temp',
    11:	'temp',
    12:	'temp',
    13:	'temp'
}
pin_names = {
    'b_1': 15,
    'b_2': 16,
    'b_3': 7,
    'b_4': 8,
    'r_1': 10,
    'r_2': 11,
    'r_3': 12,
    'end_program_pin': 13
}

# Time in milliseconds
pin_debounce_time = 35

# ---------------------------------------------- #
# 				Functions


def button_callback(channel):
    global last_pin_clicked, videos_dictionary
    if last_pin_clicked != channel:
        video_title = videos_dictionary.get(channel, "Invalid Channel")
        print('./test.sh ' + video_title + '.mp4')
        subprocess.call("./test.sh ../" + video_title + ".mp4", shell=True)
        last_pin_clicked = channel


def pin(name_of_pin):
    global pin_names
    return pin_names.get(name_of_pin, -1)


# ---------------------------------------------- #

print('Starting gpio_test.py')

# Set up the GPIO pin numbering system
# BOARD is the position on the board
# BCM is the numbering of the GPIO
GPIO.setmode(GPIO.BOARD)

# Setup all the pins
GPIO.setup(pin('end_program_pin'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(pin('b_1'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('b_1'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)
GPIO.setup(pin('b_2'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('b_2'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)
GPIO.setup(pin('b_3'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('b_3'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)
GPIO.setup(pin('b_4'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('b_4'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)
GPIO.setup(pin('r_1'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('r_1'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)
GPIO.setup(pin('r_2'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('r_2'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)
GPIO.setup(pin('r_3'), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pin('r_3'), GPIO.RISING,
                      callback=button_callback, bouncetime=pin_debounce_time)

print('Pin setup complete')

# Pause and let the computer catch up
# Number in seconds
time.sleep(0.5)

# Main Loop
# The control scheme of this program is callback function interrupts for
# each button

# This just has the program run until the 'END' button is pressed
# That button will be inside the control pannel, away from prying eyes
GPIO.wait_for_edge(pin('end_program_pin'), GPIO.RISING)

print('Closing gpio_test.py')

# Cleanup *all* resources used at the end of the sketch
# This should always be done at the end!
GPIO.cleanup()
