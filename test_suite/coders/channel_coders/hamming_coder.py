from test_suite.coders.channel_coders._channel_coder import ChannelCoder
from test_suite.helper_types import Bits, Probabilities


def to_bit(probability: float) -> int:
    return 1 if probability > 0.5 else 0


class HammingChannelCoder(ChannelCoder):

    def __init__(self):
        super().__init__("Hamming")

    def encode(self, data: Bits) -> Bits:
        if len(data) % 4 != 0:
            raise ValueError("Data length must be a multiple of 4")

        encoded = []
        for i in range(0, len(data), 4):
            d = data[i:i + 4]
            d1 = d[0]
            d2 = d[1]
            d3 = d[2]
            d4 = d[3]
            encoded.extend([
                d1 ^ d2 ^ d4,  # P1
                d1 ^ d3 ^ d4,  # P2
                d1,  # D1
                d2 ^ d3 ^ d4,  # P3
                d2,  # D2
                d3,  # D3
                d4  # D4
            ])

        return encoded

    def decode(self, data: Probabilities) -> Bits:
        decoded = []
        for i in range(0, len(data), 7):
            d = data[i:i + 7]
            p1 = to_bit(d[0])
            p2 = to_bit(d[1])
            d1 = to_bit(d[2])
            p3 = to_bit(d[3])
            d2 = to_bit(d[4])
            d3 = to_bit(d[5])
            d4 = to_bit(d[6])

            p1_ = d1 ^ d2 ^ d4
            p2_ = d1 ^ d3 ^ d4
            p3_ = d2 ^ d3 ^ d4

            error_index = 0
            if p1 != p1_:
                error_index += 1
            if p2 != p2_:
                error_index += 2
            if p3 != p3_:
                error_index += 4

            if error_index == 3:
                d1 = 1 - d1
            elif error_index == 5:
                d2 = 1 - d2
            elif error_index == 6:
                d3 = 1 - d3
            elif error_index == 7:
                d4 = 1 - d4

            decoded.extend([d1, d2, d3, d4])

        return decoded
