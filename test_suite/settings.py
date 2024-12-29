

class Settings:
    sample_width: int
    bit_duration_in_ms: float
    sample_rate: int
    
    def __init__(self, sample_width: int, bit_duration_in_ms: float, sample_rate: int):
        self.sample_width = sample_width
        self.bit_duration_in_ms = bit_duration_in_ms
        self.sample_rate = sample_rate
    
    @property
    def bit_duration_in_sec(self) -> float:
        return self.bit_duration_in_ms / 1000
    
    @property
    def bits_per_sec(self) -> float:
        return 1 / self.bit_duration_in_sec
    
    @property
    def samples_per_bit(self) -> float:
        return self.bit_duration_in_sec * self.sample_rate
    
    @property
    def max_amplitude(self) -> int:
        return 2 ** (self.sample_width * 8 - 1) - 1
    