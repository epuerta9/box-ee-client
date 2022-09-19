
#
# code was used from https://github.com/dupontgu/ch559-circuitpython/blob/main/ch559.py
#

#
# Keycodes were used from adafruit HID library 
#


MSG_START =               0xFE
LINE_DELIM =              0x0A

MSG_TYPE_CONNECTED =      0x01
MSG_TYPE_DISCONNECTED =   0x02
MSG_TYPE_ERROR =          0x03
MSG_TYPE_DEVICE_POLL =    0x04
MSG_TYPE_DEVICE_STRING =  0x05
MSG_TYPE_DEVICE_INFO =    0x06
MSG_TYPE_HID_INFO =       0x07
MSG_TYPE_STARTUP =        0x08

DEVICE_TYPE_KYBRD =       0x06
DEVICE_TYPE_MOUSE =       0x02

CODE_CTRL_L =             0xE0
CODE_SHIFT_L =            0xE1
CODE_ALT_L =              0xE2
CODE_GUI_L =              0xE3
CODE_CTRL_R =             0xE4
CODE_SHIFT_R =            0xE5
CODE_ALT_R =              0xE6
CODE_GUI_R =              0xE7

# modifier keys are compressed into a single byte, these are the bit indices (from LSB)
MOD_BIT_FLAG_MAP = {
    0: CODE_CTRL_L,
    1: CODE_SHIFT_L,
    2: CODE_ALT_L, 
    3: CODE_GUI_L,
    4: CODE_CTRL_R,
    5: CODE_SHIFT_R,
    # right side GUI button (Windows/CMD) doesn't seem to work with CH559 fw?
    7: CODE_ALT_R
}

class Ch559:
    def __init__(self, uart):
        self._cached_keys = []
        self._uart = uart
        self._incomplete_data = None
    
    def poll(self):
        # reused from  code was used from https://github.com/dupontgu/ch559-circuitpython/blob/main/ch559.py
        # conveniently, the ch559 spits out packets delimited with newline chars
        # BUT the newline value (0x0a) may also be part of the data packet being sent
        # so we use uart.readline for conevience, but we still wait for the full expected packet length
        data = self._uart.readline()
        if data is not None:
            if data[0] == MSG_START:
                self._incomplete_data = None
            elif self._incomplete_data is not None:
                data = self._incomplete_data + data
            msg_data_len = data[1]
            if len(data) == msg_data_len + 12:
                return self.parse(data)
            else: 
                self._incomplete_data = data

    def parse(self, packet):
        msg_len = packet[1]
        msg_type = packet[3]
        if msg_type != MSG_TYPE_DEVICE_POLL:
            return
        device_type = packet[4]
        if device_type == DEVICE_TYPE_KYBRD:
            return self.get_data(packet)

    def get_data(self, packet):
        modifier_flags = packet[11]
        modifer_keys_pressed = []
        for i in range(8):
            has_mod_for_index = (modifier_flags & (1 << i)) > 0
            if has_mod_for_index:
                mod_code = MOD_BIT_FLAG_MAP.get(i)
                if mod_code is not None:
                    modifer_keys_pressed.append(mod_code)
        # for some reason, certain keys come with the 7th highest bit randomly set
        # no idea what the 64 offset is for - I just observed that these values were 64 higher than CircuitPython's Keycodes
        keys_pressed = [(0b10111111 & i) - 64 if i >= 0x80 else (0b00111111 & i) for i in packet[13:18] if i > 0] + modifer_keys_pressed
        
        return  KEY_CODES[keys_pressed[0]] if keys_pressed else None



class Scanner:

    def __init__(self):
        pass


    async def run(self, async_sleep):

        while True:

            await async_sleep(5)


KEY_CODES = {
    4 : 'A',
    5 : 'B',
    6: 'C',
    7 : 'D',
    8 : 'E',
    9 : 'F',
    10 : 'G',
    11 : 'H',
    12 : 'I',
    13 : 'J',
    14 : 'K',
    15 : 'L',
    16 : 'M',
    17 : 'N',
    18 : 'O',
    19 : 'P',
    20 : 'Q',
    21 : 'R',
    22 : 'S',
    23 : 'T',
    24 : 'U',
    25 : 'V',
    26 : 'W', 
    27 : 'X', 
    28 : 'Y',
    29 : 'Z',
    30 : '1',
    31 : '2',
    32 : '3',
    33 : '4',
    34 : '5',
    35 : '6',
    36 : '7',
    37 : '8',
    38 : '9',
    39 : '0',
    40 : 'ENTER'

}
