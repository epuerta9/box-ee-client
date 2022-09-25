"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""

from lib.app import build_app, blink_success_app, blink_fail_app

from machine import UART, Pin
import sys
import uasyncio

interruptCounter = 0

LED_BUILTIN = 2

def main():
    #Start box-ee device program

    #uart interface for barcode scanner
    uart = UART(1,400000, rx=18, tx=19)

    #pin for lock 
    lock_pin = Pin(0, Pin.OUT)
    reset_button = Pin(4, Pin.IN)

    built_in_led = Pin(LED_BUILTIN, Pin.OUT)

    app = build_app(uart=uart, lock_pin=lock_pin, reset_button=reset_button, built_in_led=built_in_led)
    try:
        app.ping()
        blink_success_app(built_in_led)
    except Exception as err:
        blink_fail_app(built_in_led)
        print(f"error pinging server: {err}")
        sys.exit(1)

        
    uasyncio.run(app.run())

#    blink_success()
#    #check connectivity
#    if app.ping().get('msg') != 'ok':
#        blink_fail()
#        raise Exception("unable to ping api.box-ee.com")


        

main()

