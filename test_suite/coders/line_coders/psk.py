import math
import time

from pydub import AudioSegment

from test_suite.coders.line_coders._line_coder import LineCoder
from test_suite.settings import Settings
from test_suite.helper_types import Bits, Probabilities


class BinaryPskLineCoder(LineCoder):
    frequency: int

    def __init__(self, settings: Settings, frequency: int):
        super().__init__("BPSK", settings)
        self.frequency = frequency

    def encode(self, data: Bits) -> AudioSegment:
        samples_count = int(len(data) * self.settings.samples_per_bit)
        samples_per_bit = samples_count // (len(data))
        samples_count = samples_per_bit * len(data)

        wave_data = bytearray()
        bit_index = -1
        for i in range(samples_count):
            if i % samples_per_bit == 0:
                bit_index += 1

            bit = data[bit_index]
            t = i / self.settings.sample_rate
            sample = self.settings.max_amplitude * math.cos(2 * math.pi * self.frequency * t + bit * math.pi)
            wave_data.extend(
                int.to_bytes(int(sample), length=self.settings.sample_width, signed=True, byteorder="little"))

        return AudioSegment(
            data=bytes(wave_data),
            sample_width=self.settings.sample_width,
            frame_rate=self.settings.sample_rate,
            channels=1
        )

    def decode(self, audio: AudioSegment) -> Probabilities:
        samples = audio.get_array_of_samples()
        bits = []
        for i in range(0, len(samples), int(self.settings.samples_per_bit)):
            t = i / self.settings.sample_rate

            I = samples[i] * math.cos(2 * math.pi * self.frequency * t)
            Q = samples[i] * math.sin(2 * math.pi * self.frequency * t)

            phase = math.atan2(Q, I)

            bits.append(1 if abs(phase) > math.pi / 2 else 0)

        return bits


class QuadPskLineCoder(LineCoder):
    frequency: int

    def __init__(self, settings: Settings, frequency: int):
        super().__init__("QPSK", settings)
        self.frequency = frequency

    def encode(self, data: Bits) -> AudioSegment:
        if len(data) % 2 != 0:
            raise ValueError("Data length must be even for QPSK encoding.")

        samples_count = int(len(data) * self.settings.samples_per_bit // 2)
        samples_per_symbol = samples_count // (len(data) // 2)
        samples_count = samples_per_symbol * (len(data) // 2)

        wave_data = bytearray()
        symbol_index = -1

        for i in range(samples_count):
            if i % samples_per_symbol == 0:
                symbol_index += 1
                # Extract two bits for each symbol
                bit_pair = data[symbol_index * 2:symbol_index * 2 + 2]
                symbol_value = (bit_pair[0] << 1) | bit_pair[1]  # Convert to integer (0-3)
                phase = symbol_value * math.pi / 2

            t = i / self.settings.sample_rate
            sample = self.settings.max_amplitude * math.cos(2 * math.pi * self.frequency * t + phase)
            wave_data.extend(
                int.to_bytes(int(sample), length=self.settings.sample_width, signed=True, byteorder="little")
            )

        return AudioSegment(
            data=bytes(wave_data),
            sample_width=self.settings.sample_width,
            frame_rate=self.settings.sample_rate,
            channels=1
        )

    def decode(self, audio: AudioSegment) -> Bits:
        samples = audio.get_array_of_samples()
        bits = []
        samples_per_symbol = int(self.settings.samples_per_bit)

        for i in range(0, len(samples), samples_per_symbol):
            t = i / self.settings.sample_rate

            I = sum(samples[i + k] * math.cos(2 * math.pi * self.frequency * (t + k / self.settings.sample_rate))
                    for k in range(samples_per_symbol))
            Q = sum(samples[i + k] * math.sin(2 * math.pi * self.frequency * (t + k / self.settings.sample_rate))
                    for k in range(samples_per_symbol))

            phase = math.atan2(Q, I)

            # Map phase to symbol value
            if -math.pi / 4 <= phase < math.pi / 4:
                symbol = 0  # 00
            elif math.pi / 4 <= phase < 3 * math.pi / 4:
                symbol = 3  # 01
            elif -3 * math.pi / 4 <= phase < -math.pi / 4:
                symbol = 1  # 11
            else:
                symbol = 2  # 10

            # Convert symbol back to two bits
            bits.append((symbol >> 1) & 1)  # First bit
            bits.append(symbol & 1)         # Second bit

        return bits