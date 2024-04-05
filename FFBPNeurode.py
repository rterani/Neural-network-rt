from FFNeurode import FFNeurode
from BPNeurode import BPNeurode


class FFBPNeurode(FFNeurode, BPNeurode):
    def __init__(self):
        """Initialize FFNeurode and BPNeurode"""
        FFNeurode.__init__(self)
        BPNeurode.__init__(self)
