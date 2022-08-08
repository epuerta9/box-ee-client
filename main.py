"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""
from lib.repo import Repo, WIFI_PASSWORD_KEY, WIFI_SSID_KEY, DEVICE_API_KEY
from lib.wireless.access_point import web_page 
from lib.app import App
from lib.pinpad import PinPad
import network
from machine import disable_irq, enable_irq, Pin
import json


interruptCounter = 0

def delete(repo):
    repo.delete(WIFI_SSID_KEY)
    repo.delete(WIFI_PASSWORD_KEY)
    repo.flush()
    repo.close()
    gc.collect()

def main():
    #check if btree info is populated
    with open("config.json") as f:
        config = json.load(f)
    version = config["meta"]["version"]
    print(f"version: {version}")  
    repo = Repo()
    if repo.check_wireless_credentials():
        #credentials found lets try and connect to the wifi

        ssid = repo.get(WIFI_SSID_KEY)
        password = repo.get(WIFI_PASSWORD_KEY)
        api_key = repo.get(DEVICE_API_KEY)

        gc.collect()
        print("Connecting to wifi...")

        counter=0
        # Activate the station interface
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        # Connect to your wifi network
        print("ssid: ")
        print(ssid)
        print("password")
        print(password)
        try:
            sta_if.connect(ssid, password)
        except OSError as err:
            delete(repo=repo)
            print(err)
            machine.reset()

        import time
        while not sta_if.isconnected():
            print("connecting.. ")
            counter += 1
            time.sleep(1)
            if counter > 15:
#                #incorrect credentials, delete existing credentials and soft_reset
                delete(repo=repo)
                print("unable to connect to wifi... resetting")
                machine.reset()


        # Print out the network configuration received from DHCP
        
        print('network config:', sta_if.ifconfig())
        repo.close()
        #Start box-ee device program
        app = App(api_key=api_key, conf=config)
        pad = PinPad()
        global interruptCounter
        pound_key_pin = pad.col_pins[2]
        pound_key_pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)
        while True:
            if interruptCounter > 0:
                state = disable_irq()
                interruptCounter = interruptCounter-1
                pass_codes = pad.scan_keys()
                print(pass_codes)
                pinkey = ",".join(pass_codes)
                print("to be validated: ", pinkey)
                enable_irq(state)
    
    else:
        web_page()

def callback(pin):
    global interruptCounter


main()

