from pydub import AudioSegment
from test_suite.noises._noise import Noise


class Channel:
    name: str
    noises: list[tuple[Noise, int]]

    def __init__(self, name: str, noises: list[tuple[Noise, int]]):
        self.name = name
        self.noises = noises

    def transmit(self, audio: AudioSegment) -> AudioSegment:
        for noise, amplification in self.noises:
            noise_audio = noise.create(audio)
            audio = audio.overlay(noise_audio + amplification)
        return audio
