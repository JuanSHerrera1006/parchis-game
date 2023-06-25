class Cell:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.is_grabbed = False

    def has_piece(self):
        return self.piece != None

    def set_piece(self, piece):
        self.piece = piece

    def quit_piece(self):
        self.piece = None
