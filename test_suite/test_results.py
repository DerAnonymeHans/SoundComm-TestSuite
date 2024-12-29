import numpy as np
import scipy
from pydub import AudioSegment

from test_suite.helper_types import Bits


def calculate_bit_error_rate(error_mask: Bits) -> float:
    return sum(error_mask) / len(error_mask)


def calculate_avg_error_length(error_mask: Bits) -> float:
    error_lengths = []
    error_length = 0
    for bit in error_mask:
        if bit == 1:
            error_length += 1
            continue

        if error_length > 0:
            error_lengths.append(error_length)
            error_length = 0

    if error_length > 0:
        error_lengths.append(error_length)

    avg_error_length = 0 if len(error_lengths) == 0 else sum(error_lengths) / len(error_lengths)
    return avg_error_length


def get_error_mask(sent_bits: Bits, received_bits: Bits) -> Bits:
    error_mask = []
    for sent_bit, received_bit in zip(sent_bits, received_bits):
        error_mask.append(0 if sent_bit == received_bit else 1)
    return error_mask


def is_error_distribution_random(error_mask: Bits, alpha: float) -> bool:
    runs = 1
    for i in range(1, len(error_mask)):
        if round(error_mask[i]) != round(error_mask[i - 1]):
            runs += 1

    expected_runs = (len(error_mask) + 1) / 2
    expected_varianz = (len(error_mask) - 1) / 4
    c = scipy.stats.norm.ppf(1 - alpha / 2)
    test_value = (runs - expected_runs) / expected_varianz ** 0.5
    return abs(test_value) < c


class TestCaseRepetitionResult:
    sent_bits: Bits
    received_bits: Bits
    received_signal: AudioSegment
    error_mask: Bits

    def __init__(self, sent_bits: Bits, received_bits: Bits, received_signal: AudioSegment):
        self.sent_bits = sent_bits
        self.received_bits = received_bits
        self.received_signal = received_signal
        self.error_mask = get_error_mask(sent_bits, received_bits)


class TestCaseResult:
    channel_name: str
    coder_name: str

    repetitions: list[TestCaseRepetitionResult]

    bit_error_rate: float
    avg_error_length: float
    error_count: int
    error_distribution_random: bool
    bits_per_second: float

    def __init__(self, channel_name: str, coder_name: str, repetitions: list[TestCaseRepetitionResult]):
        self.channel_name = channel_name
        self.coder_name = coder_name
        self.repetitions = repetitions

        self.bit_error_rate = 0
        self.avg_error_length = 0
        self.error_count = 0
        error_distribution_random_count = 0
        self.bits_per_second = 0

        for repetition in repetitions:
            self.bit_error_rate += calculate_bit_error_rate(repetition.error_mask)
            self.avg_error_length += calculate_avg_error_length(repetition.error_mask)
            self.error_count += sum(repetition.error_mask)
            error_distribution_random_count += 1 if is_error_distribution_random(repetition.error_mask, alpha=0.05) else 0
            self.bits_per_second += len(repetition.sent_bits) / repetition.received_signal.duration_seconds

        self.bit_error_rate /= len(repetitions)
        self.avg_error_length /= len(repetitions)
        self.error_count /= len(repetitions)
        self.error_distribution_random = True if error_distribution_random_count > len(repetitions) / 2 else False
        self.bits_per_second /= len(repetitions)
        
    def error_mask(self):
        np_arrays = [np.array(repetition.error_mask) for repetition in self.repetitions]
        return np.sum(np_arrays, axis=0)


class TestResult:
    test_name: str
    case_results: list[TestCaseResult]

    def __init__(self, test_name: str, test_case_results: list[TestCaseResult]):
        self.test_name = test_name
        self.case_results = test_case_results
