from test_suite.helper_types import Bits


def bytes_to_bits(data: bytes) -> Bits:
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits: Bits) -> bytearray:
    bytes = bytearray()
    for i in range(len(bits)):
        if i % 8 == 0:
            bytes.append(0)
        bytes[-1] |= bits[i] << (i % 8)
    return bytes