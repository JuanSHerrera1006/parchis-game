from board import Board
from constants import CELL_SIZE
from dragger import Dragger
import pygame

class Game():
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.players = []
        self.current_player = None
        self.dice = []
        self.clock = pygame.time.Clock()

    def handle_events(self, screen):
        board = self.board
        dragger = self.dragger

        if dragger.dragging:
            dragger.update_blit(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragger.update_mouse(event.pos)
                
                clicked_row = dragger.mouseX // CELL_SIZE
                clicked_col = dragger.mouseY // CELL_SIZE

                if board.cells[clicked_row][clicked_col].has_piece():
                    piece = board.cells[clicked_row][clicked_col].piece
                    dragger.save_initial(event.pos)
                    dragger.drag_piece(piece)

            elif event.type == pygame.MOUSEMOTION:
                if dragger.dragging:
                    dragger.update_mouse(event.pos)
                    self.render(screen)
                    dragger.update_blit(screen)
            
            elif event.type == pygame.KEYUP:
                pass

            elif event.type == pygame.MOUSEBUTTONUP:
                dragger.undrag_piece()

            elif event.type == pygame.QUIT:
                return False
        pygame.display.update()
        return True

    def render(self, screen):
        self.board.render(screen, self.dragger)

