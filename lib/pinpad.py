
from machine import Pin, lightsleep
import uasyncio
import time


KEY_MATRIX = [
    '1','2','3','A',
    '4','5','6','B',
    '7','8','9','C',
    '*','0','#','D'
]

#POUND_KEY_ICON = KEY_MATRIX[3][2]

KEY_ROWS = [21,22,23,25]
KEY_COLS = [12,13,14,15]

KEY_UP          = 0
KEY_DOWN        = 1
KEY_DOWN_LONG   = 2
KEY_UP_LONG     = 3  

GLOBAL_SCAN_INTERRUPT = True

class PinPad:
    
    def __init__(self, lock, async_validate_func, built_in_led):
       


        #initialize all to state up
        self.keys = [ { 'char':key_var, 'state': KEY_UP} for key_var in KEY_MATRIX ] 
        self.row_pins = [Pin(KEY_ROWS[idx], Pin.OUT) for idx, x in enumerate(KEY_ROWS)]
        self.col_pins = [Pin(KEY_COLS[idx], Pin.IN, Pin.PULL_DOWN, value=0) for idx, x in enumerate(KEY_COLS)]
        self.pass_code = []
        self._async_validate_func = async_validate_func
        self._lock = lock
        self._built_in_led = built_in_led

    def blink_scanner_success(self, led):
        led.on()
        time.sleep(3)
        led.off()
        lightsleep()

    def blink_scanner_fail(self, led):
        for _ in range(3):
            led.on()
            time.sleep(.5)
            led.off()
            time.sleep(.5)
        lightsleep()

    async def scan_coro(self):
        """A coroutine to scan each row and check column for key events."""
       
        while True:
            key_code = 0
            for row, row_pin in enumerate(self.row_pins):
                ## Assert row.
                row_pin.value(1)
                ## Delay between processing each row.
                ## Check for key events for each column of current row.
                for col, col_pin in enumerate(self.col_pins):
                    ## Process pin state.
                    key = self.keys[key_code]
                    key_event = None
                    if col_pin.value():
                        ## key state is UP
                        if key['state'] == KEY_UP:
                            print(f"pressed {key}")
                            ## just pressed (up => down)
                            key_event = KEY_DOWN
                            key['state'] = key_event
                    else:
                        ## key not pressed (up)
                        if key['state'] == KEY_DOWN:
                            ## just released (down => up)
                            key_event = KEY_UP 
                            key['state'] = key_event         
                    
                    ## Process key event.
                    if key_event == KEY_UP:
                        key_char = self.keys[key_code]['char']
                        self.pass_code.append(key_char)
                        if len(self.pass_code) == 4:
                            print(f"sending to api {self.pass_code}")
                            pass_string = ''.join(self.pass_code)
                            print(f"string: {pass_string}")
                            try:
                                response = self._async_validate_func(pass_string)
                                if response.get("valid"):
                                    self._lock.unlock()
                                    await uasyncio.sleep(5)
                                    self._lock.lock()
                                    self.blink_scanner_success(self._built_in_led)
                                    self.pass_code = []
                                else:
                                   self.blink_scanner_fail(self._built_in_led) 
                            finally:
                                #clean the pass code
                                self.pass_code = []
                            
                    key_code += 1

                ## Deassert row.
                row_pin.value(0)
            await uasyncio.sleep_ms(1)
        
