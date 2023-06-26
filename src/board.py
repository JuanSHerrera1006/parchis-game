from player import Piece, Player
from constants import *
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

    def check_rival_pos(self, new_pos, coords, piece):
        if new_pos in SECURE_CELLS:
            return None

        for coord in coords:
            if self.cells[coord[0]][coord[1]].has_piece():
                other_piece = self.cells[coord[0]][coord[1]].piece
                if other_piece.color != piece.color:
                    return coord
        return None

    def meta_move(self, dragger, valid_moves):
        piece = dragger.piece
        META_MAP = GOALS[piece.color]
        cond = piece.acc >= 80
        cell_numb, _ = piece.get_actual_pos(cond)
        
        if cell_numb == 10:
            piece.state = Piece.STATE_OUT_GAME
            return

        possible_mov = [(cell_numb + dice_result) % META_CELLS[piece.color] for dice_result in valid_moves]
        map_coord = [(None, None) if i > 10 else (i, META_MAP[i]) for i in possible_mov]

        drag_row = dragger.mouseX // CELL_SIZE
        drag_col = dragger.mouseY // CELL_SIZE

        for new_pos, coords in map_coord:
            if new_pos == None and coords == None:
                continue

            for coord in coords:
                row = coord[0]
                col = coord[1]

                mouse_pos = (drag_row, drag_col)
                next_cell_mov = self.cells[row][col]

                if mouse_pos == coord and not next_cell_mov.has_piece():
                    selected_dice = new_pos - cell_numb if cond else new_pos + 1
                    Board.plays.remove(selected_dice)
                    piece.acc += selected_dice
                    self.move_piece(piece, mouse_pos)
                    break

    def normal_move(self, dragger):
        piece = dragger.piece
        cell_numb, _ = piece.get_actual_pos()
        possible_mov = [(cell_numb + dice_result) % 84 for dice_result in Board.plays]
        map_coord = [(i, BOARD_MAP[i]) for i in possible_mov]
        
        drag_row = dragger.mouseX // CELL_SIZE
        drag_col = dragger.mouseY // CELL_SIZE
        
        for new_pos, coords in map_coord:
            check_enemy_pos = self.check_rival_pos(new_pos, coords, piece)
            for coord in coords:
                row = coord[0]
                col = coord[1]
                if (drag_row, drag_col) == coord:
                    if check_enemy_pos != None:
                        other_piece = self.cells[check_enemy_pos[0]][check_enemy_pos[1]].piece
                        for pos in INITIAL_POS[other_piece.color]:
                            pos_row, pos_col = pos
                            if not self.cells[pos_row][pos_col].has_piece():
                                other_piece.state = Piece.STATE_CAPTURED
                                self.move_piece(other_piece, pos)
                                self.cells[check_enemy_pos[0]][check_enemy_pos[1]].quit_piece() 
                                break

                        selected_dice = new_pos - piece.get_actual_pos()[0]
                        selected_dice = 84 - piece.get_actual_pos()[0] + new_pos if selected_dice < 0 else selected_dice
                        Board.plays.remove(selected_dice)
                        self.move_piece(piece, (drag_row, drag_col))
                        piece.acc += selected_dice
                        break
                    
                    selected_dice = new_pos - piece.get_actual_pos()[0]
                    selected_dice = 84 - piece.get_actual_pos()[0] + new_pos if selected_dice < 0 else selected_dice
                    new_pos = (drag_row, drag_col) if not self.cells[row][col].has_piece() and check_enemy_pos == None else piece.coord 
                    
                    if piece.coord != new_pos:
                        Board.plays.remove(selected_dice)

                    self.move_piece(piece, new_pos)
                    piece.acc += selected_dice
                    break
                break

    def valid_move(self, dragger):
        piece = dragger.piece
        while Board.plays:
            valid_moves = list(filter(lambda dice_result: piece.acc + dice_result >= 80, Board.plays))
            if valid_moves and piece.state == Piece.STATE_IN_GAME: self.meta_move(dragger, valid_moves)
            else: self.normal_move(dragger)
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

