import urequests as requests
import ujson as json
from machine import Pin
import time
import gc
from  lib.lock import Lock, LOCK_PIN
from lib.scanner import Scanner
from lib.pinpad import PinPad
import network
from lib.repo import Repo, WIFI_PASSWORD_KEY, WIFI_SSID_KEY, DEVICE_API_KEY
from lib.wireless.access_point import web_page 
from uasyncio import run, create_task, sleep



LED_BUILTIN = 2
p_builtin = Pin(2, Pin.OUT)

class App:

    def __init__(self, api_key, conf, **kw):

        self.endpoint = conf["config"]["endpoint"]
        self.healthcheck = conf["config"]["healthcheck"]
        self.api_key = api_key
        self.build_pinpad = conf["config"]["features"].get("pinpad", False)
        self.build_scanner = conf["config"]["features"].get("scanner", False)
        self._uart = kw.get("uart")
        self._lock_pin = kw.get("lock_pin")

    def ping(self):
        response = requests.get(self.healthcheck, headers= {'Content-Type' : 'application/json'}).json()
        return response


    def validate_pin(self, pin_code):
        """
        validate pin code
        """
        try:
            url = self.endpoint + "?pinkey=" + pin_code
            headers = {
                "Content-Type" : "application/json",
                "X-Boxee-ClientToken" : self.api_key
            }
            response = requests.get(url, headers=headers).json()
            print(response)
            return response
        except Exception as err:
            print(err)

    def run(self):
        """
        asyncio run attachments
        """
        tasks = []

        #build lock
        if not self._lock_pin:
            raise Exception("missing pin object for lock")
        lock = Lock(self._lock_pin)
        if self.build_pinpad:
            pinpad = PinPad()

            tasks.append(create_task(pinpad.run(sleep)))

        if self.build_scanner:
            if not self._uart:
                raise Exception("uart object missing")
            scanner = Scanner(self._uart, async_validate_func=self.validate_pin, lock=lock)
            tasks.append(scanner.run(sleep))
        
        run(*tasks)

def build_app(**kw):
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
                blink_fail()
                machine.reset()


        # Print out the network configuration received from DHCP
        
        print('network config:', sta_if.ifconfig())
        blink_success()
        repo.close()
        return App(api_key=api_key, conf=config, **kw)
    else:
        web_page()


        

    
def delete(repo):
    repo.delete(WIFI_SSID_KEY)
    repo.delete(WIFI_PASSWORD_KEY)
    repo.flush()
    repo.close()
    gc.collect()

def blink_success():
    for i in range(0,3):
        p_builtin.on()
        p_builtin.off()
        time.sleep(1)


def blink_fail():
    p_builtin.on()
    time.sleep(5)

    