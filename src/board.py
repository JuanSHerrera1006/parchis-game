from constants import *
from player import Piece
import pygame
import os

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

class Board:
    plays = []

    def __init__(self, players):
        self.cells = []
        self.background_image = pygame.image.load(os.path.join(os.path.pardir, BOARD_IMAGE_PATH))
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_SIZE, SCREEN_SIZE))
        self.players = players
        self._load_board()
        self._load_pieces()
 
    def _load_board(self):
        self.cells = [[Cell(row * CELL_SIZE, col * CELL_SIZE) for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]

    def _load_pieces(self): 
        # Get players
        player_blue = self.players[0]
        player_red = self.players[1]
        player_green = self.players[2]
        player_yellow = self.players[3]
        
        # Fichas amarillas
        self.cells[26][24].set_piece(player_yellow.pieces[0])
        self.cells[26][26].set_piece(player_yellow.pieces[1])
        self.cells[24][24].set_piece(player_yellow.pieces[2])
        self.cells[24][26].set_piece(player_yellow.pieces[3])

        # Fichas rojas
        self.cells[3][3].set_piece(player_red.pieces[0])
        self.cells[5][3].set_piece(player_red.pieces[1])
        self.cells[3][5].set_piece(player_red.pieces[2])
        self.cells[5][5].set_piece(player_red.pieces[3])

        # Fichas verdes
        self.cells[24][3].set_piece(player_green.pieces[0])
        self.cells[26][3].set_piece(player_green.pieces[1])
        self.cells[24][5].set_piece(player_green.pieces[2])
        self.cells[26][5].set_piece(player_green.pieces[3])

        # Fichas azul
        self.cells[3][26].set_piece(player_blue.pieces[0])
        self.cells[5][26].set_piece(player_blue.pieces[1])
        self.cells[3][24].set_piece(player_blue.pieces[2])
        self.cells[5][24].set_piece(player_blue.pieces[3])

    def move_piece(self, piece, new_pos):
        row, col = piece.coord
        piece.coord = new_pos
        self.cells[row][col].quit_piece()
        self.cells[new_pos[0]][new_pos[1]].set_piece(piece)


    def valid_move(self, dragger):
        piece = dragger.piece
        while Board.plays:
            possible_mov = [(piece.get_actual_pos() + dice_result) % 84 for dice_result in Board.dices_result]
            map_coord = [(i, BOARD_MAP[i]) for i in possible_mov]
            
            drag_row = dragger.mouseX // CELL_SIZE
            drag_col = dragger.mouseY // CELL_SIZE
            
            for idx, coord in map_coord:
                if (drag_row, drag_col) == coord:
                    selected_dice = idx - piece.get_actual_pos()
                    selected_dice = 84 - piece.get_actual_pos() + idx if selected_dice < 0 else selected_dice
                    self.move_piece(piece, (drag_row, drag_col))
                    Board.plays.remove(selected_dice)
                    break
            break
 
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

