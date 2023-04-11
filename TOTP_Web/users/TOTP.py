from .sha1 import Sha1


class TOTP:

    def __init__(self, hmac_key, key_length, time_step=30):
        self._hmac_key = hmac_key
        self._key_length = key_length
        self._time_step = time_step
        self._byte_array = bytearray(8)

    def get_code(self, time_stamp):
        steps = time_stamp // self._time_step
        return self.get_code_from_steps(int(steps))

    def get_code_from_steps(self, steps):
        sha = Sha1()
        _byte_array = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        _byte_array[4] = int((steps >> 24) & 0xFF)
        _byte_array[5] = int((steps >> 16) & 0xFF)
        _byte_array[6] = int((steps >> 8) & 0xFF)
        _byte_array[7] = int((steps & 0xFF))

        sha.initHmac(self._hmac_key, self._key_length)
        sha.write(_byte_array)
        _hash = sha.resultHmac()

        _offset = _hash[20 - 1] & 0xF
        _truncated_hash = 0
        for j in range(4):
            _truncated_hash <<= 8
            _truncated_hash |= _hash[_offset + j]

        _truncated_hash &= 0x7FFFFFFF
        _truncated_hash %= 1000000

        _code = "{:06d}".format(_truncated_hash)
        return _code
