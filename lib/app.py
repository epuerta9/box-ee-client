
import urequests as requests
from  lib.lock import Lock, LOCK_PIN
from lib.pinpad import PinPad
from esp32 import wake_on_ext0, WAKEUP_ANY_HIGH


class App:

    def __init__(self, api_key, conf):

        self.endpoint = conf["config"]["endpoint"]
        self.healthcheck = conf["config"]["healthcheck"]
        self.api_key = api_key

    def validate_pin(self, pin_code):
        """
        validate pin code
        """
        pass

    def validate_code(self, code):
        """
        validates scanned in tracking code
        """
        pass


        
    


    
    