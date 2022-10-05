import urequests as requests
import ujson as json
import machine
import time
import gc
from  lib.lock import Lock
from lib.scanner import Scanner
from lib.pinpad import PinPad 
import network
from lib.repo import Repo, WIFI_PASSWORD_KEY, WIFI_SSID_KEY, DEVICE_API_KEY
from lib.wireless.access_point import web_page 
from uasyncio import get_event_loop, sleep_ms, sleep



class App:

    def __init__(self, api_key, conf, repo, **kw):

        self.endpoint = conf["config"]["endpoint"]
        self.healthcheck = conf["config"]["healthcheck"]
        self.api_key = api_key
        self.build_pinpad = conf["config"]["features"].get("pinpad", False)
        self.build_scanner = conf["config"]["features"].get("scanner", False)
        self._uart = kw.get("uart")
        self._lock_pin = kw.get("lock_pin")
        self._reset_button = kw.get("reset_button")
        self._built_in_led = kw.get("built_in_led")
        self._repo = repo

    def ping(self):
        try:
            response = requests.get(self.healthcheck, headers= {'Content-Type' : 'application/json'}).json()
            print(f"ping response: {response}")
        except Exception as err:
            print(err)
            print("unable to ping box-ee api")
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
            print(f"successful response: {response}")
            return response
        except Exception as err:
            blink_fail_app(self._built_in_led)
            print(f"error: {err}")
            return None

    def run(self):
        """
        asyncio run attachments
        """
        print("starting box-ee client")
        loop = get_event_loop()
        #build lock
        if not self._lock_pin:
            raise Exception("missing pin object for lock")
        lock = Lock(self._lock_pin)

        if self.build_pinpad:
            pinpad = PinPad(lock, self.validate_pin, built_in_led=self._built_in_led)

            loop.create_task(pinpad.scan_coro())
            print("created pinpad coroutine task")

        if self.build_scanner:
            if not self._uart:
                raise Exception("uart object missing")
            scanner = Scanner(self._uart, async_validate_func=self.validate_pin, lock=lock, built_in_led=self._built_in_led)
            loop.create_task(scanner.run())
            print("created scanner coroutine task")
        
        if self._reset_button:
           loop.create_task(reset_watcher(self._reset_button, self._repo)) 
           print("created reset button task")

        #setup wake up sensor
        loop.create_task(light_sleep_timer())
        print("created light sleep timer task")

        #run loop
        loop.run_forever()

async def light_sleep_timer():
    while True:
        await sleep(180)
        print("going into light sleep")
        machine.lightsleep()

async def reset_watcher(button, repo):

    while True:
        if button.value():
            delete(repo)
            time.sleep(1)
            machine.reset()

        await sleep_ms(1)

        

def build_app(**kw):
    built_in_led = kw.get("built_in_led")
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
                blink_fail_app(built_in_led)
                machine.reset()


        # Print out the network configuration received from DHCP
        
        print('network config:', sta_if.ifconfig())
        blink_success_app(built_in_led)
        repo.close()
        return App(api_key=api_key, conf=config, repo=repo, **kw)
    else:
        web_page()


def blink_success_app(led):
    led.on()
    time.sleep(3)
    led.off()


def blink_fail_app(led):
    led.on()
    time.sleep(5)
    led.off()
    time.sleep(2)

    
def delete(repo):
    repo.delete(WIFI_SSID_KEY)
    repo.delete(WIFI_PASSWORD_KEY)
    repo.delete(DEVICE_API_KEY)
    repo.flush()
    repo.close()
    gc.collect()


    