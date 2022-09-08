"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""

from lib.app import build_app, blink_success, blink_fail


interruptCounter = 0


def main():
    #Start box-ee device program
    app = build_app()
    blink_success()
    #check connectivity
    if app.ping().get('msg') != 'ok':
        blink_fail()
        raise Exception("unable to ping api.box-ee.com")

    pad = PinPad()
    while True:
        pass_codes = pad.scan_keys()
        print(pass_codes)
        pinkey = ",".join(pass_codes)
        print("to be validated: ", pinkey)
        gc.collect()
        

main()

