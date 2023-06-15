
class Piece:
    # Create state constants
    STATE_AVAILABLE = 0
    STATE_CAPTURED = 1
    STATE_OUT_GAME = -1 

    def __init__(self, color, state=STATE_AVAILABLE):
        self.color = color
        self.state = state


    def move(self):
        pass

    def captured(self, piece):
        pass

