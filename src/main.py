from constants import *
from game import Game
import pygame
import sys

class Main:
    def __init__(self):
        self.screen = None
        self.is_running = True
        self.options = {"dice_sides": 6, "dice_num": 2}
        self.game = Game()

    def menu(self):    
        MENU_PROMPT = """--- MENU PRINCIPAL ---
        Opciones:

        1) Partida Normal
        2) Modo batalla
        3) Exit

        La opcion que has elegido es: """

        while (userInput := input(MENU_PROMPT)) != '3':
            if userInput == '1':
                self.set_opts()
            elif userInput == '2':
                pass
            else:
                print('Has ingresado una opcion no valida')

    def set_opts(self):
        sides = int(input("Digita el numero de lados del dado: "))
        numb = int(input("Digita el numero de dados con los que deseas jugar: "))
        self.opt = {"dices_sides": sides, "dices_numb": numb}
        self._init_game()
        self.loop()

    def _init_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Parchis")

    def loop(self):
        game = self.game
        game.set_dices(self.opt["dices_sides"], self.opt["dices_numb"])

        while self.is_running:
            self.is_running = game.handle_events(self.screen)
            game.render(self.screen)
            game.clock.tick(60)
        pygame.quit()
        sys.exit()
            
main = Main()
main.menu()
