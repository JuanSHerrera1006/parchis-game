from constants import BOARD_MAP, CELL_SIZE, PIECE_IMAGE_PATHS, INITIAL_POS
from random import randint
import os
import pygame


class Player:
    def __init__(self, playerId, color):
        self.playerId = playerId
        self.color = color
        self.pieces = []
        self._load_pieces()

    def _load_pieces(self):
        positions = INITIAL_POS[self.color]
        for idx, pos in enumerate(positions):
            pieceId = f"player0{self.playerId}_{self.color}{idx}"
            piece = Piece(pieceId, self.color, pos)
            self.pieces.append(piece)

class Piece:
    # Create state constants
    STATE_CAPTURED = 0
    STATE_IN_GAME = 1
    STATE_OUT_GAME = -1 

    def __init__(self, pieceId, color, coord, texture_rect = None, state=STATE_CAPTURED):
        self.pieceId = pieceId
        self.color = color
        self.coord = coord
        self.texture_rect = texture_rect
        self.texture = os.path.join(os.path.pardir, PIECE_IMAGE_PATHS[self.color]) 
        self.state = state

    def get_actual_pos(self):
        row, col = self.coord
        for cell_numb, coord in BOARD_MAP.items():
            row_map = coord[0]
            col_map = coord[1]
            if row_map == row and col_map == col:
                return cell_numb
        return None

    def render(self, x, y, screen, size=(30, 30)):
        img = pygame.image.load(self.texture)
        img = pygame.transform.scale(img, size) 
        img_center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        self.texture_rect = img.get_rect(center=img_center)
        screen.blit(img, self.texture_rect)

class Dice: 
    def __init__(self, sides):
        self.sides = sides

    def calculate_result(self):
        return randint(1, self.sides)
