class Square:
    DEFAULT = [None, None, None]

    def __init__(self, row, col, pieces=DEFAULT):
        self.row = row
        self.col = col
        self.pieces = pieces

