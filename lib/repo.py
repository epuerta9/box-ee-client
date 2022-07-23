import btree

WIFI_SSID_KEY = "wifi_ssid_key".encode()
WIFI_USERNAME_KEY = "wifi_username_key".encode()
WIFI_PASSWORD_KEY = "wifi_password_key".encode()


WIFI_CONSTANTS = [WIFI_PASSWORD_KEY,WIFI_SSID_KEY,WIFI_USERNAME_KEY]

class RepoStatusCodes:
    EMPTY_REPO = 1
    CREDENTIALS_FOUND = 2


class Repo:

    def __init__(self):
        try:
            self.f = open("localstore.db", "r+b")
        except OSError:
            self.f = open("localstore.db", "w+b")
        self.db = btree.open(self.f)

    def add(self,ssid, username, password):
        """
        add to the btree, must be of type bytes
        """
        if isinstance(password, str):
            password = password.encode()
        if isinstance(username, str):
            username = username.encode()
        if isinstance(ssid, str):
            ssid = ssid.encode()

        self.db[WIFI_SSID_KEY] = ssid
        self.db[WIFI_USERNAME_KEY] = username
        self.db[WIFI_PASSWORD_KEY] = password

    def get(self, key):
        """
        get the key value from the db
        """
        if key not in WIFI_CONSTANTS:
            raise Exception("invalid key")
        return self.db[key]

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
            return RepoStatusCodes.EMPTY_REPO
        
        for key in self.db:
            if key not in WIFI_CONSTANTS:
                raise Exception(f"key not found: {key}")
            
        return RepoStatusCodes.CREDENTIALS_FOUND

