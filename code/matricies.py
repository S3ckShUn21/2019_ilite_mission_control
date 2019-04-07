import RPi.GPIO as GPIO
import time
from threading import Thread

# This will be the object that controls turning the lights on
class LEDMatrix():
    def __init__(self, keys, row_pins, col_pins, gpio_mode=GPIO.BOARD):
        self._keys = keys
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._name_index = {}

        # Searching through the array everytime is really slow
        # This creates a hashmap basically for what led row and col to turn on
        self._setupNameIndex()

        # Set the matrix pins as outputs
        self._setupPins(gpio_mode)

    def _setupNameIndex(self):
        # Num rows
        for i in range(len(self._keys)):
            # Num cols
            for j in range(len(self._keys[0])):
                # Adds a dictionary entry with the coordinate of the value
                self._name_index[self._keys[i][j]] = (i, j)

    def _setupPins(self, gpio_mode):
        if GPIO.getmode() is not gpio_mode:
            # Setup all of the pins as outputs
            GPIO.setmode(gpio_mode)

        # First do the columns; they will be driven low, therefore they have a pullUP resistor
        for pin in self._col_pins:
            print("Turning on pin " + str(pin))
            GPIO.setup(pin, GPIO.OUT)

        # Second do the rows; rows will be driven high, therefore 'normal mode' is pullDOWN
        for pin in self._row_pins:
            print("Turning on pin " + str(pin))
            GPIO.setup(pin, GPIO.OUT)

    # Figure out the pin numbers to drive high/low
    # time on is seconds for the light to stay on
    def _turnOnLED(self, ledName, timeOn):
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

    # Turn the led on ON A DIFFERENT THREAD because it will be on for a set amount of time
    # We don't want it impeading the main clock cycle
    def driveLED(self, ledName, timeOn=5):
        Thread(target=self._turnOnLED, args=(ledName,timeOn)).start()


# Object that handles reading the buttons
class ButtonMatrix():
    def __init__(self, keys, row_pins, col_pins, callback_function, gpio_mode=GPIO.BOARD):
        self._keys = keys
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._callback_function = callback_function
        self._poll_thread = None
        self._is_polling = True
        self._name_index = {}

        # Searching through the array everytime is really slow
        # This creates a hashmap basically for what led row and col to turn on
        self._setupNameIndex()

        # Set the matrix pins as outputs
        self._setupPins(gpio_mode)

        # Start polling the buttons
        self._poll_thread = Thread(target=self._poll)
        self._poll_thread.start()

    # relate pin values pairs to their respective pin name
    def _setupNameIndex(self):
        # Num rows
        for i in range(len(self._keys)):
            # Num cols
            for j in range(len(self._keys[0])):
                # takes the row and col physical pin num in a tuple - sets it equal to the name
                self._name_index[(self._row_pins[i], self._col_pins[j])] = self._keys[i][j]

    def _setupPins(self, gpio_mode):
        if GPIO.getmode() is not gpio_mode:
            # Setup all of the pins as outputs
            GPIO.setmode(gpio_mode)

        # First do the columns; They will be inputs; active HIGH (physical pulldown is required)
        for pin in self._col_pins:
            print("Turning on pin " + str(pin))
            GPIO.setup(pin, GPIO.IN)

        # Second do the rows; rows will be driven high
        for pin in self._row_pins:
            print("Turning on pin " + str(pin))
            GPIO.setup(pin, GPIO.OUT)

    # This polling will happen in a different thread
    def _poll(self):
        while self._is_polling:
            # Power on each row
            for row in self._row_pins:
                GPIO.output(row, GPIO.HIGH)
                # Check for which column is powered
                for col in slef._col_pins:
                    if GPIO.input(col) == GPIO.HIGH:
                        # If a button is powered then pass the button name to the callback function
                        self._callback_function(self._name_index[(row,col)])
            # Poll 20 times per second
            time.sleep(0.050)

    def cleanupMatrix(self):
        self._is_polling = False
        self._poll_thread.join()
        GPIO.cleanup()
