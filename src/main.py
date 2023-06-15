from constants import *
from game import Game
import pygame
import sys


class Main:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Parchis")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game()

    def loop(self):
        while True:
            self.game.show_bg(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.loop()
