"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""

from lib.app import build_app



interruptCounter = 0

LED_BUILTIN = 2


def main():
    #Start box-ee device program
    app = build_app()

    #check connectivity
    if not app.ping():
        raise Exception("unable to ping api.box-ee.com")
    pad = PinPad()
    while True:
        pass_codes = pad.scan_keys()
        print(pass_codes)
        pinkey = ",".join(pass_codes)
        print("to be validated: ", pinkey)
        app.validate_pin(pinkey)
        gc.collect()
        

main()

