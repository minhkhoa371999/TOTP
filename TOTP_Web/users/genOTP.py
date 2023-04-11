
import datetime
from TOTP import TOTP

hmacKey = [0x4d, 0x79, 0x4c, 0x65, 0x67, 0x6f, 0x44, 0x6f, 0x6f, 0x72]

b = datetime.datetime(2023, 3, 22, 6, 00, 2)

def genOTP(now, serial):
    encoded_string = serial.encode()
    byte_array = bytearray(encoded_string)
    key = hmacKey+list(byte_array)
    totp = TOTP(key, 10)
    b_ts = int(b.timestamp())
    now_ts = int(now.timestamp())
    gmt = int(now_ts - b_ts)
    code = ''
    new_code = totp.get_code(gmt)
    if code != new_code:
        code = new_code
    return code
