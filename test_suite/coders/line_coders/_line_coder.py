from pydub import AudioSegment

from test_suite.settings import Settings
from test_suite.helper_types import Probabilities, Bits


class LineCoder:
    name: str
    settings: Settings
    
    def __init__(self, name: str, settings: Settings):
        self.name = name
        self.settings = settings

    def encode(self, data: Bits) -> AudioSegment:
        raise NotImplementedError()
    
    def decode(self, data: AudioSegment) -> Probabilities:
        raise NotImplementedError()