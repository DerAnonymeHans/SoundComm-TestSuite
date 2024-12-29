from test_suite.helper_types import Bits, Probabilities


class ChannelCoder:
    name: str

    def __init__(self, name: str):
        self.name = name

    def encode(self, data: Bits) -> Bits:
        raise NotImplementedError()

    def decode(self, data: Probabilities) -> Bits:
        raise NotImplementedError()


class NoChannelCoder(ChannelCoder):
    
    def __init__(self):
        super().__init__("NoChannelCoder")
    
    def encode(self, data: Bits) -> Bits:
        return data

    def decode(self, data: Probabilities) -> Bits:
        bits = []
        for probability in data:
            bits.append(1 if probability > 0.5 else 0)
        return bits
