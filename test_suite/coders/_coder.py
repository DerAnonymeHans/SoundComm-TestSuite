from pydub import AudioSegment

from test_suite.coders.channel_coders._channel_coder import ChannelCoder
from test_suite.helper import bytes_to_bits
from test_suite.coders.line_coders._line_coder import LineCoder
from test_suite.helper_types import Bits


class Coder:
    channel_coder: ChannelCoder
    line_coder: LineCoder
    name: str

    def __init__(self, channel_coder: ChannelCoder, line_coder: LineCoder, name: str | None = None):
        self.channel_coder = channel_coder
        self.line_coder = line_coder
        self.name = name if name is not None else f"{self.channel_coder.name} -> {self.line_coder.name}"

    def encode_bytes(self, data: bytes) -> AudioSegment:
        return self.encode(bytes_to_bits(data))

    def encode(self, data: Bits) -> AudioSegment:
        encoded_data = self.channel_coder.encode(data)
        return self.line_coder.encode(encoded_data)

    def decode(self, audio: AudioSegment) -> Bits:
        decoded_data = self.line_coder.decode(audio)
        return self.channel_coder.decode(decoded_data)
    
