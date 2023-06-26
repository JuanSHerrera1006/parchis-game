from constants import BOARD_MAP, CELL_SIZE, GOALS, PIECE_IMAGE_PATHS, INITIAL_POS
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
        self.acc = 0

    def get_actual_pos(self, next_moves=[]):

        cond = [next_move + self.acc >= 80 for next_move in next_moves]
        items = GOALS[self.color].items() if any(cond) else BOARD_MAP.items()

        for cell_numb, coords in items:
            for idx, coord in enumerate(coords, start=0):
                if self.coord == coord: 
                    return (cell_numb, idx)
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
