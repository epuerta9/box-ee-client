
LOCK_PIN = 0

class Lock:

    def __init__(self, pin):
        self.pin = pin

    def lock(self):
        self.pin.on()
    
    def unlock(self):
        self.pin.off()