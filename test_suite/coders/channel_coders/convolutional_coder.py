from test_suite.coders.channel_coders._channel_coder import ChannelCoder
from test_suite.helper_types import Bits, Probabilities


class ConvolutionalChannelCoder(ChannelCoder):
    
    def __init__(self):
        super().__init__("ConvolutionalChannelCoder")
    
    def encode(self, data: Bits) -> Bits:
        
        
        
        return data
    
    def decode(self, data: Probabilities) -> Bits:
        pass