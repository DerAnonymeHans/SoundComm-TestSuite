import random

from pydub import AudioSegment

from test_suite.noises._noise import Noise


class AWGN(Noise):
    
    def __init__(self):
        super().__init__("AWGN")

    def create(self, audio: AudioSegment) -> AudioSegment:
        noise = random.randbytes(int(audio.frame_count()) * audio.frame_width)
        noise_audio = AudioSegment(data=bytes(noise), sample_width=audio.sample_width, frame_rate=audio.frame_rate,
                                   channels=audio.channels)
        
        return noise_audio
