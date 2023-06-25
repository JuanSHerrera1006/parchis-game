from constants import *
from piece import Piece
from cell import Cell
import pygame
import os

class Board:
    def __init__(self):
        self.cells = []
        self.background_image = pygame.image.load(os.path.join(os.path.pardir, BOARD_IMAGE_PATH))
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_SIZE, SCREEN_SIZE))
        self._load_board()
        self._load_pieces()
 
    def _load_board(self):
        self.cells = [[Cell(row * CELL_SIZE, col * CELL_SIZE) for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]

    def _load_pieces(self):
        # Fichas amarillas
        self.cells[26][24].set_piece(Piece("yellow"))
        self.cells[26][26].set_piece(Piece("yellow"))
        self.cells[24][24].set_piece(Piece("yellow"))
        self.cells[24][26].set_piece(Piece("yellow"))

        # Fichas rojas
        self.cells[3][3].set_piece(Piece("red"))
        self.cells[5][3].set_piece(Piece("red"))
        self.cells[3][5].set_piece(Piece("red"))
        self.cells[5][5].set_piece(Piece("red"))

        # Fichas verdes
        self.cells[24][3].set_piece(Piece("green"))
        self.cells[26][3].set_piece(Piece("green"))
        self.cells[24][5].set_piece(Piece("green"))
        self.cells[26][5].set_piece(Piece("green"))

        # Fichas azul
        self.cells[3][26].set_piece(Piece("blue"))
        self.cells[5][26].set_piece(Piece("blue"))
        self.cells[3][24].set_piece(Piece("blue"))
        self.cells[5][24].set_piece(Piece("blue"))

    def render(self, screen, dragger):
        # Render board background 
        screen.blit(self.background_image, (0, 0))
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Get coordinates
                x = self.cells[row][col].row
                y = self.cells[row][col].col

                if self.cells[row][col].has_piece():
                    piece = self.cells[row][col].piece
                    if piece is not dragger.piece:
                        piece.render(x, y, screen)

