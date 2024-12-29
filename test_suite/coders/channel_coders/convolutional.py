from enum import IntEnum
from itertools import groupby

from test_suite.coders.channel_coders._channel_coder import ChannelCoder
from test_suite.helper_types import Bits, Probabilities

class State(IntEnum):
    S00 = 0
    S01 = 1
    S10 = 2
    S11 = 3

class Path:
    hamming_dst: int
    states: list[State]
    inputs: list[int]
    
    def __init__(self, hamming_dst: int = 0, states: list[State] = [], inputs: list[int] = []):
        self.hamming_dst = hamming_dst
        self.states = states
        self.inputs = inputs
        
class Transition:
    new_state: State
    output: list[int]
    input: int
    
    def __init__(self, new_state: State, output: list[int], input: int):
        self.new_state = new_state
        self.output = output
        self.input = input

def get_hamming_dst(list_a: list[int], list_b: list[int]) -> int:
    return sum([1 if a != b else 0 for a, b in zip(list_a, list_b)])

def probs_to_bits(data: Probabilities) -> Bits:
    return [1 if bit > 0.5 else 0 for bit in data]



class ViterbiChannelCoder(ChannelCoder):

    transitions = {
        State.S00: [Transition(State.S00, [0, 0], 0), Transition(State.S10, [1, 1], 1)],
        State.S10: [Transition(State.S01, [0, 1], 0), Transition(State.S11, [1, 0], 1)],
        State.S01: [Transition(State.S00, [1, 1], 0), Transition(State.S10, [0, 0], 1)],
        State.S11: [Transition(State.S01, [1, 0], 0), Transition(State.S11, [0, 1], 1)]
    }

    def __init__(self):
        super().__init__("Viterbi")

    def encode(self, data: Bits) -> Bits:
        encoded = []
        states = [0, 0]
        for bit in data:
            c0 = bit ^ states[1]
            c1 = bit ^ states[0] ^ states[1]
            encoded.extend([c0, c1])
            states = [bit, states[0]]

        return encoded

    def decode(self, data: Probabilities) -> Bits:
        data = probs_to_bits(data)
        paths = [
            Path(states=[State.S00], hamming_dst=0, inputs=[]),
        ]

        for t in range(0, len(data) // 2):
            new_paths = []
            i = 2 * t
            for path in paths:
                for transition in self.transitions[path.states[-1]]:
                    new_path = Path(
                        states=path.states + [transition.new_state],
                        hamming_dst=path.hamming_dst + get_hamming_dst(data[i:i+2], transition.output),
                        inputs=path.inputs + [transition.input]
                    )
                    new_paths.append(new_path)

            # Eliminate paths at same end state that have higher hamming distance
            new_paths.sort(key=lambda path: int(path.states[-1]))
            grouped_by_last_state = {
                key: list(group) for key, group in groupby(new_paths, lambda path: path.states[-1])
            }

            paths = []
            for last_state in grouped_by_last_state:
                min_hamming_dst = min(path.hamming_dst for path in grouped_by_last_state[last_state])
                for path in grouped_by_last_state[last_state]:
                    if path.hamming_dst == min_hamming_dst:
                        paths.append(path)
                        break

        min_hamming_dst = min(path.hamming_dst for path in paths)
        for path in paths:
            if path.hamming_dst == min_hamming_dst:
                return path.inputs            