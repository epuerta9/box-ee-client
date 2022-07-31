from lib.repo import Repo, WIFI_PASSWORD_KEY, WIFI_SSID_KEY

repo = Repo()
repo.delete(WIFI_SSID_KEY)


repo.delete(WIFI_PASSWORD_KEY)


repo.flush()


repo.close()


gc.collect()