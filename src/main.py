from constants import *
from game import Game
import pygame
import sys

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Parchis")
        self.is_running = True
        self.game = Game()

    def loop(self):
        game = self.game

        while self.is_running:
            self.is_running = game.handle_events(self.screen)
            game.render(self.screen)
            game.clock.tick(60)
        pygame.quit()
        sys.exit()
            

main = Main()
main.loop()
