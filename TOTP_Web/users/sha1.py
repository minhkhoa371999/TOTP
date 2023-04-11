import numpy

SHA1_K0 = 0x5a827999
SHA1_K20 = 0x6ed9eba1
SHA1_K40 = 0x8f1bbcdc
SHA1_K60 = 0xca62c1d6

sha1InitState = [
    0x01, 0x23, 0x45, 0x67,  # H0
    0x89, 0xab, 0xcd, 0xef,  # H1
    0xfe, 0xdc, 0xba, 0x98,  # H2
    0x76, 0x54, 0x32, 0x10,  # H3
    0xf0, 0xe1, 0xd2, 0xc3  # H4
]

HMAC_IPAD = 0x36
HMAC_OPAD = 0x5c

BLOCK_LENGTH = 64
HASH_LENGTH = 20


class _buffer:
    def __init__(self):
        self.b = [0] * BLOCK_LENGTH
        self.w = bytearray(BLOCK_LENGTH // 4)


class _state:
    def __init__(self):
        self.b = [0] * (HASH_LENGTH)
        self.w = bytearray(HASH_LENGTH // 4)


class Sha1:
    def __init__(self):
        self.buffer_offset = 0
        self.byte_count = 0
        self.buffer = _buffer()
        self.state = _state()
        self.state.b = sha1InitState.copy() * HASH_LENGTH

    def rol32(self, number, bits):
        return ((number << bits) | (number >> (32 - bits)))

    def hashBlock(self):
        a = self.state.w[0]
        b = self.state.w[1]
        c = self.state.w[2]
        d = self.state.w[3]
        e = self.state.w[4]
        for i in range(80):
            if i >= 16:
                t = self.buffer.w[(i + 13) & 15] ^ self.buffer.w[(i + 8) & 15] ^ self.buffer.w[(i + 2) & 15] ^ \
                    self.buffer.w[i & 15]
                self.buffer.w[i & 15] = self.rol32(t, 1)

            if i < 20:
                t = (d ^ (b & (c ^ d))) + SHA1_K0
            elif i < 40:
                t = (b ^ c ^ d) + SHA1_K20
            elif i < 60:
                t = ((b & c) | (d & (b | c))) + SHA1_K40
            else:
                t = (b ^ c ^ d) + SHA1_K60

            t += self.rol32(a, 5) + e + self.buffer.w[i & 15]
            e = d
            d = c
            c = self.rol32(b, 30)
            b = a
            a = t

        w0 = self.state.w[0] + a
        w1 = self.state.w[1] + b
        w2 = self.state.w[2] + c
        w3 = self.state.w[3] + d
        w4 = self.state.w[4] + e
        self.state.w = numpy.array([w0, w1, w2, w3, w4])
        self.state.w = self.state.w.tobytes()

    def addUncounted(self, data):
        i = self.buffer_offset ^ 3
        b = list(self.buffer.b)
        b[i] = data
        self.buffer.b = b

        # self.buffer.b = numpy.array(b).tobytes()
        self.buffer_offset += 1
        if self.buffer_offset == BLOCK_LENGTH:
            self.hashBlock()
            self.buffer_offset = 0

    def write(self, data):
        self.byte_count += 1
        self.addUncounted(data)
        return 1

    def pad(self):
        # Implement SHA-1 padding (fips180-2 §5.1.1)

        # Pad with 0x80 followed by 0x00 until the end of the block
        self.addUncounted(0x80)
        while self.buffer_offset != 56:
            self.addUncounted(0x00)

        # Append length in the last 8 bytes
        self.addUncounted(0)  # We're only using 32 bit lengths
        self.addUncounted(0)  # But SHA-1 supports 64 bit lengths
        self.addUncounted(0)  # So zero pad the top bits
        self.addUncounted(self.byte_count >> 29)  # Shifting to multiply by 8
        self.addUncounted(self.byte_count >> 21)  # as SHA-1 supports bitstreams as well as
        self.addUncounted(self.byte_count >> 13)  # byte.
        self.addUncounted(self.byte_count >> 5)
        self.addUncounted(self.byte_count << 3)

    # Note that in Python, there is no need for the uint8_t type,
    # as Python has its own bytes type for representing binary
    # data. Additionally, the state variable has been converted
    # from a uint32_t state[5] array to a Python bytearray object,
    # so the accessor method .b has been changed to .tobytes().
    def result(self):
        # Pad to complete the last block
        self.pad()

        # Swap byte order back
        for i in range(5):
            a = self.state.w[i]
            b = (a << 24) | ((a << 8) & 0x00ff0000) | ((a >> 8) & 0x0000ff00) | (a >> 24)
            w = list(self.state.w)
            w[i] = b
            self.state.w = w

        # Return pointer to hash (20 characters)
        return self.state.b

    def initHmac(self, key, keyLength):
        self.keyBuffer = [0] * BLOCK_LENGTH
        if keyLength > BLOCK_LENGTH:
            self.__init__()
            for i in range(keyLength):
                self.write(key[i])
            self.keyBuffer = self.result() * HASH_LENGTH
        else:
            self.keyBuffer = key * keyLength

        self.__init__()

        for i in range(BLOCK_LENGTH):
            self.write(self.keyBuffer[i] ^ HMAC_IPAD)

    def resultHmac(self):
        innerHash = self.result()
        self.__init__()
        for i in range(BLOCK_LENGTH):
            self.write(self.keyBuffer[i] ^ HMAC_OPAD)
        for i in range(HASH_LENGTH):
            self.write(innerHash[i])
        return self.result()
