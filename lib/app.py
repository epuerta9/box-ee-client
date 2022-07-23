import os
import json
import urequests as requests


class App:

    def __init__(self, api_key, conf):

        #check if config file exists
        try:
            os.stat("config.json")
        except OSError as err:
            print(err)
            raise Exception("config file: config.json does not exist")
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


        
    

def run_app(config):
    pass