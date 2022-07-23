"""
main.py will be responsible for running the main program which runs through the following checks 

* checks if wireless information is stored in local btree
** if wireless info is stored, try and connect to wifi. 
** if not, run as AccessPoint with webpage for wireless credentials

"""
from lib.repo import Repo, RepoStatusCodes, WIFI_PASSWORD_KEY, WIFI_SSID_KEY
from lib.wireless.access_point import web_page 
from lib.app import run_app
import network
import sys
import machine
import json



def main():
    #check if btree info is populated
    with open("config.json") as f:
        config = json.load(f)
    version = config["meta"]["version"]
    print(f"version: {version}")  
    repo = Repo()
    is_populated = repo.check_wireless_credentials()
    if is_populated == RepoStatusCodes.CREDENTIALS_FOUND:
        #credentials found lets try and connect to the wifi

        ssid = repo.get(WIFI_SSID_KEY)
        password = repo.get(WIFI_PASSWORD_KEY)
        repo.close()

        gc.collect()

        print("Connecting to wifi...")
        counter=0
        # Activate the station interface
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        # Connect to your wifi network
        sta_if.connect(ssid, password)
        if counter > 15:
            #incorrect credentials, delete existing credentials and soft_reset
            repo.delete(WIFI_SSID_KEY)
            repo.delete(WIFI_PASSWORD_KEY)
            machine.soft_reset()
        while not sta_if.isconnected():
            counter += 1
        # Print out the network configuration received from DHCP
        
        print('network config:', sta_if.ifconfig())

        #Start package place device program
        run_app(config)

    else:
        #start web server
        web_page()

if __name__ == '__main__':
    main()

