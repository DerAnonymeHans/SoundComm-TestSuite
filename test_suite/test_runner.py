import time

import scipy
from pydub.playback import play

from test_suite.channels._channel import Channel
from test_suite.coders._coder import Coder
from test_suite.helper import bytes_to_bits
from test_suite.helper_types import Bits
from test_suite.test_results import TestResult, TestCaseResult, TestCaseRepetitionResult
from test_suite.test_visualization import visualize_test_result


class Test:
    test_name: str
    data: bytes
    channels: list[Channel]
    coders: list[Coder]

    def __init__(self, name: str, data: bytes, channels: list[Channel], coders: list[Coder]):
        self.test_name = name
        self.data = data
        self.channels = channels
        self.coders = coders

    @property
    def name(self) -> str:
        return ""


class TestRunner:
    results: list[TestResult]
    play_audio: bool
    repetitions: int

    def __init__(self, play_audio: bool = False, repititions: int = 1):
        self.results = []
        self.play_audio = play_audio
        self.repetitions = repititions

    def run(self, test: Test) -> TestResult:
        case_results = []
        for channel in test.channels:
            for coder in test.coders:
                case_repetitions_results = []
                for rep in range(self.repetitions):
                    case_repetition_result = self.run_test_case_repitition(test.data, channel, coder)
                    case_repetitions_results.append(case_repetition_result)
                case_result = TestCaseResult(channel_name=channel.name, coder_name=coder.name, repetitions=case_repetitions_results)
                case_results.append(case_result)

        test_result = TestResult(test_name=test.test_name, test_case_results=case_results)
        self.results.append(test_result)
        return test_result

    def run_test_case_repitition(self, data: bytes, channel: Channel, coder: Coder) -> TestCaseRepetitionResult:
        bits = bytes_to_bits(data)
        sent_signal = coder.encode(bits)
        received_signal = channel.transmit(sent_signal)
        if self.play_audio:
            play(received_signal)
        received_bits = coder.decode(received_signal)
        return TestCaseRepetitionResult(sent_bits=bits, received_bits=received_bits, received_signal=received_signal)

    def show_results(self):
        for test_result in self.results:
            visualize_test_result(test_result)
