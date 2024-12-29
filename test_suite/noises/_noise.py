from pydub import AudioSegment


class Noise:
    
    name: str
    
    def __init__(self, name: str):
        self.name = name
    
    def create(self, audio: AudioSegment) -> AudioSegment:
        raise NotImplementedError()
