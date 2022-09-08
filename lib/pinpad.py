
from machine import Pin


KEY_MATRIX = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']
]

POUND_KEY_ICON = KEY_MATRIX[3][2]

KEY_ROWS = [21,22,23,25]
KEY_COLS = [12,13,14,15]

GLOBAL_SCAN_INTERRUPT = True

class PinPad:
    
    def __init__(self):

        self.row_pins = [Pin(KEY_ROWS[idx], Pin.OUT, value=1) for idx, x in enumerate(KEY_ROWS)]
        self.col_pins = [Pin(KEY_COLS[idx], Pin.IN, Pin.PULL_DOWN, value=0) for idx, x in enumerate(KEY_COLS)]
        self.pass_code = []

    async def run(self, async_sleep):
        if self.pass_code:
            self.pass_code.clear()
        while True:
            for i, row in enumerate(self.row_pins):
                for j, col in enumerate(self.col_pins):
                    row.on()
                    if col.value() == 1:
                        print("you have pressed: ", KEY_MATRIX[i][j])
                        self.pass_code.append(KEY_MATRIX[i][j])
                        if len(self.pass_code) == 4:
                            print(self.pass_code)
                            self.pass_code.clear()
                row.off()
            await async_sleep(5)
    
