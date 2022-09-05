import urequests as requests
import ujson as json
import gc
from  lib.lock import Lock, LOCK_PIN
from lib.pinpad import PinPad
import network
from lib.repo import Repo, WIFI_PASSWORD_KEY, WIFI_SSID_KEY, DEVICE_API_KEY
from lib.wireless.access_point import web_page 

class App:

    def __init__(self, api_key, conf):

        self.endpoint = conf["config"]["endpoint"]
        self.healthcheck = conf["config"]["healthcheck"]
        self.api_key = api_key

    def ping(self):
        response = requests.get(self.healthcheck, headers= {'Content-Type' : 'application/json'}).json()
        return response

        
    def validate_pin(self, pin_code):
        """
        validate pin code
        """
        try:
            url = self.endpoint + "?pinkey=" + pin_code
            response = requests.get(url).json()
            print(response)
        except Exception as err:
            print(err)

    def validate_code(self, code):
        """
        validates scanned in tracking code
        """
        pass

def build_app():
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
        return App(api_key=api_key, conf=config)
    else:
        web_page()


        

    
def delete(repo):
    repo.delete(WIFI_SSID_KEY)
    repo.delete(WIFI_PASSWORD_KEY)
    repo.flush()
    repo.close()
    gc.collect()



    
    