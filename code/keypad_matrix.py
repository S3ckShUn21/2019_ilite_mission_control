#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from threading import Timer, Thread

DEFAULT_KEY_DELAY = 300
DEFAULT_REPEAT_DELAY = 1.0
DEFAULT_REPEAT_RATE = 1.0
DEFAULT_DEBOUNCE_TIME = 10


class KeypadFactory():

    def create_keypad(self, keypad=None, row_pins=None, col_pins=None, key_delay=DEFAULT_KEY_DELAY, repeat=False, repeat_delay=None, repeat_rate=None, gpio_mode=GPIO.BCM):

        if keypad is None:
            keypad = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                ["*", 0, "#"]
            ]

        if row_pins is None:
            row_pins = [4, 14, 15, 17]

        if col_pins is None:
            col_pins = [18, 27, 22]

        return Keypad(keypad, row_pins, col_pins, key_delay, repeat, repeat_delay, repeat_rate, gpio_mode)

    def create_4_by_3_keypad(self):

        KEYPAD = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            ["*", 0, "#"]
        ]

        ROW_PINS = [4, 14, 15, 17]
        COL_PINS = [18, 27, 22]

        return self.create_keypad(KEYPAD, ROW_PINS, COL_PINS)

    def create_4_by_4_keypad(self):

        KEYPAD = [
            [1, 2, 3, "A"],
            [4, 5, 6, "B"],
            [7, 8, 9, "C"],
            ["*", 0, "#", "D"]
        ]

        ROW_PINS = [4, 14, 15, 17]
        COL_PINS = [18, 27, 22, 23]

        return self.create_keypad(KEYPAD, ROW_PINS, COL_PINS)


class Keypad():
    def __init__(self, keypad, row_pins, col_pins, key_delay=DEFAULT_KEY_DELAY, repeat=False, repeat_delay=None, repeat_rate=None, gpio_mode=GPIO.BOARD):
        self._handlers = []

        self._current_active_row = 0
        self._row_thread = None
        self._row_thread_running = False
        self._keypad = keypad
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._key_delay = key_delay
        self._repeat = repeat
        self._repeat_delay = repeat_delay
        self._repeat_rate = repeat_rate
        self._repeat_timer = None
        if repeat:
            self._repeat_delay = repeat_delay if repeat_delay is not None else DEFAULT_REPEAT_DELAY
            self._repeat_rate = repeat_rate if repeat_rate is not None else DEFAULT_REPEAT_RATE
        else:
            if repeat_delay is not None:
                self._repeat = True
                self._repeat_rate = repeat_rate if repeat_rate is not None else DEFAULT_REPEAT_RATE
            elif repeat_rate is not None:
                self._repeat = True
                self._repeat_delay = repeat_delay if repeat_delay is not None else DEFAULT_REPEAT_DELAY

        self._last_key_press_time = 0
        self._first_repeat = True

        GPIO.setmode(gpio_mode)

        self._setRowsAsOutput()
        self._setColumnsAsInput()

        self._row_thread = Thread( target=self._change_active_row_thread )
        self._row_thread_running = True
        self._row_thread.start()

        print("Keypad Inited")

    def registerKeyPressHandler(self, handler):
        self._handlers.append(handler)

    def unregisterKeyPressHandler(self, handler):
        self._handlers.remove(handler)

    def clearKeyPressHandlers(self):
        self._handlers = []

    def _change_active_row_thread(self):
        while True:
            GPIO.output(self._row_pins[self._current_active_row], GPIO.LOW)
            self._current_active_row = (self._current_active_row + 1) % len(self._row_pins)
            GPIO.output(self._row_pins[self._current_active_row], GPIO.HIGH)
            time.sleep(DEFAULT_REPEAT_RATE * 0.01)

    def _repeatTimer(self):
        print("Repeat Timer")
        self._repeat_timer = None
        self._onKeyPress(None)

    def _onKeyPress(self, pin_num):
        currTime = self.getTimeInMillis()
        if currTime < self._last_key_press_time + self._key_delay:
            return

        keyPressed = self.getKey(pin_num)
        if keyPressed is not None:
            for handler in self._handlers:
                handler(keyPressed)
            self._last_key_press_time = currTime
            if self._repeat:
                print("Starting the Timer")
                self._repeat_timer = Timer(
                    self._repeat_delay if self._first_repeat else 1.0/self._repeat_rate, self._repeatTimer)
                self._first_repeat = False
                self._repeat_timer.start()
        else:
            if self._repeat_timer is not None:
                self._repeat_timer.cancel()
            self._repeat_timer = None
            self._first_repeat = True

    def _setRowsAsOutput(self):
        # Set all rows as input
        for i in range(len(self._row_pins)):
            # GPIO.setup(self._row_pins[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # GPIO.add_event_detect(
            #     self._row_pins[i], GPIO.FALLING, callback=self._onKeyPress, bouncetime=DEFAULT_DEBOUNCE_TIME)
            GPIO.setup(self._row_pins[i], GPIO.OUT) 
            GPIO.output(self._row_pins[i], GPIO.LOW)

    def _setColumnsAsInput(self):
        # Set all columns as output low
        for j in range(len(self._col_pins)):
        #     GPIO.setup(self._col_pins[j], GPIO.OUT)
        #     GPIO.output(self._col_pins[j], GPIO.LOW)
            GPIO.setup(self._col_pins[j], GPIO.IN)
            GPIO.add_event_detect( self._col_pins[j], GPIO.RISING, callback=self._onKeyPress, bouncetime=DEFAULT_DEBOUNCE_TIME)

    def getKey(self, pin_num):

        print("Working")

        # keyVal = None

        return self._keypad[self._current_active_row][self._col_pins.index(pin_num)]
        # for i in range(len(self._row_pins)):
        #     row = self._row_pins[i]
        #     GPIO.output(row, GPIO.HIGH)

        #     for j in range(len(self._col_pins)):
        #         col = self._col_pins[j]
        #         if GPIO.input(col) == GPIO.HIGH:
        #             return self._keypad[i][j]

        # return None

    def cleanup(self):
        self._row_thread_running = False
        self._row_thread.join()

        if self._repeat_timer is not None:
            self._repeat_timer.cancel()
        GPIO.cleanup()

    def getTimeInMillis(self):
        return time.time() * 1000
