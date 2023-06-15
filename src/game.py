import pygame
from constants import *

class Game:
    def __init__(self):
        pass

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                color = None
                border_color = BLACK

                if row < 7 and col < 7 or col >= 10 and col < 13 and row < 7:            
                    color = RED

                elif row >= 16 and row <= ROWS - 1 and col < 7 or row >= 10 and row < 13 and col < 7:
                    color = BLUE

                elif col >= 16 and col <= COLS - 1 and row < 7 or col >= 16 and col <= COLS - 1 and row >= 10 and row < 13: 
                    color = GREEN

                elif row >= 16 and row <= ROWS - 1 and col >= 16 or row >= 16 and row <= ROWS - 1 and col >= 10 and col < 13:
                    color = YELLOW
                else:
                    color = WHITE


                x = col * SQSIZE
                y = row * SQSIZE

                rect = (x, y, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, border_color, rect)
                pygame.draw.rect(surface, color, (x + 1, y + 1, SQSIZE - 2, SQSIZE - 2))
