import btree

WIFI_SSID_KEY = "wifi_ssid_key".encode()
WIFI_PASSWORD_KEY = "wifi_password_key".encode()
DEVICE_API_KEY = "device_api_key".encode()


WIFI_CONSTANTS = [WIFI_PASSWORD_KEY,WIFI_SSID_KEY,DEVICE_API_KEY]



class Repo:

    def __init__(self):
        try:
            self.f = open("localstore.db", "r+b")
        except OSError:
            self.f = open("localstore.db", "w+b")
        self.db = btree.open(self.f)

    def add(self,ssid, device_api_key, password):
        """
        add to the btree, must be of type bytes
        """
        if isinstance(password, str):
            password = password.encode()
        if isinstance(device_api_key, str):
            device_api_key = device_api_key.encode()
        if isinstance(ssid, str):
            ssid = ssid.encode()

        self.db[WIFI_SSID_KEY] = ssid
        self.db[WIFI_PASSWORD_KEY] = password
        self.db[DEVICE_API_KEY] = device_api_key
        self.flush()
        self.close()
    def get(self, key):
        """
        get the key value from the db
        """
        if key not in WIFI_CONSTANTS:
            raise Exception("invalid key")
        try:
            return self.db[key].decode()
        except Exception as err:
            print(err)
            return err

    def delete(self, key):
        """
        delete to the btree, key must be of types byte
        """
        if key not in WIFI_CONSTANTS:
            raise Exception("invalid key")
        del self.db[key]

    def flush(self):
        self.db.flush()

    def close(self):
        """
        close both the file and the btree
        """
        self.db.close()
        self.f.close()

    def check_wireless_credentials(self):
        """
        checks if wireless credentials are found in the db
        """
        if len(list(self.db)) == 0:
            return False
        
        for key in self.db:
            if key not in WIFI_CONSTANTS:
                raise Exception(f"key not found: {key}")
        if WIFI_PASSWORD_KEY not in list(self.db):
            return False
        if WIFI_SSID_KEY not in list(self.db):
            return False
        return True

