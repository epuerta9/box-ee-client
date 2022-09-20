"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""

from lib.app import build_app, blink_success, blink_fail

from machine import UART, Pin

interruptCounter = 0


def main():
    #Start box-ee device program

    #uart interface for barcode scanner
    uart = UART(1,400000, rx=18, tx=19)

    #pin for lock 
    lock_pin = Pin(0, Pin.OUT)

    app = build_app(uart=uart, lock_pin=lock_pin)
    blink_success()
    #check connectivity
    if app.ping().get('msg') != 'ok':
        blink_fail()
        raise Exception("unable to ping api.box-ee.com")


        

main()

