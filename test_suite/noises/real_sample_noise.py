from pydub import AudioSegment

from test_suite.noises._noise import Noise


class RealSampleNoise(Noise):

    def create(self, audio: AudioSegment) -> AudioSegment:
        pass
