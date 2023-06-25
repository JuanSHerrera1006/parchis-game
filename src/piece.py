from constants import CELL_SIZE, PIECE_IMAGE_PATHS
import os
import pygame

class Piece:
    # Create state constants
    STATE_CAPTURED = 0
    STATE_IN_GAME = 1
    STATE_OUT_GAME = -1 

    def __init__(self, color, texture_rect = None, state=STATE_CAPTURED):
        self.color = color
        self.texture_rect = texture_rect
        self.texture = os.path.join(os.path.pardir, PIECE_IMAGE_PATHS[self.color]) 
        self.state = state

    def render(self, x, y, screen, size=(25, 25)):
        img = pygame.image.load(self.texture)
        img = pygame.transform.scale(img, size) 
        img_center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        self.texture_rect = img.get_rect(center=img_center)
        screen.blit(img, self.texture_rect)


