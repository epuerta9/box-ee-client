"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""

from lib.app import build_app, blink_success_app, blink_fail_app

from machine import UART, Pin
import sys

import esp32
interruptCounter = 0

LED_BUILTIN = 2
RESET_BUTTON = 32

def main():
    #Start box-ee device program

    #uart interface for barcode scanner
    uart = UART(1,400000, rx=18, tx=19)

    #pin for lock 
    lock_pin = Pin(0, Pin.OUT)
    reset_button = Pin(4, Pin.IN)

    built_in_led = Pin(LED_BUILTIN, Pin.OUT)

    #completely reset button
    reset_button = Pin(32, Pin.IN, Pin.PULL_UP)

    sleep_pin = Pin(33, Pin.IN)
    esp32.wake_on_ext0(pin=sleep_pin, level=esp32.WAKEUP_ANY_HIGH)

    app = build_app(uart=uart, lock_pin=lock_pin, reset_button=reset_button, built_in_led=built_in_led, reset_button=reset_button)
    try:
        app.ping()
        blink_success_app(built_in_led)
    except Exception as err:
        blink_fail_app(built_in_led)
        print(f"error pinging server: {err}")
        sys.exit(1)

        
    app.run()


        

main()

