
LOCK_PIN = 0

class Lock:

    def __init__(self, pin):
        self.pin = pin

    def unlock(self):
        self.pin.on()
    
    def lock(self):
        self.pin.off()