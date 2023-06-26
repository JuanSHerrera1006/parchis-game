from constants import CELL_SIZE, BOARD_MAP
from player import Piece, Player, Dice
from board import Board
from dragger import Dragger
from random import randint
from tkinter import Tk
from tkinter import messagebox
import pygame

class Game():
    def __init__(self):
        self.players = [Player(1, "azul"), Player(2, "rojo"), Player(3, "verde"), Player(4, "amarillo")]
        self.board = Board(self.players)
        self.dices = [Dice(6) for _ in range(2)]
        self.dices_result = []
        self.dragger = Dragger()
        self.current_player = randint(0, 3)
        self.clock = pygame.time.Clock()
        self.popUp = Tk().wm_withdraw()
        self.roll_dices()

    def next_turn(self):
        self.current_player = (self.current_player + 1) % 4
        print(f"Turno del jugador {self.players[self.current_player].color}")
        # messagebox.showinfo("Informacion del juego: ",f"Turno del jugador {self.players[self.current_player].color}")

    def roll_dices(self):
        self.dices_result = [dice.calculate_result() for dice in self.dices]
        Board.plays = self.dices_result.copy()

    def check_pair(self, dices_result):
        return len(set(dices_result)) == 1

    def check_pieces_in_game(self):
        player = self.players[self.current_player]
        for piece in player.pieces:
            if piece.state == Piece.STATE_IN_GAME:
                return True
        return False

    def show_dices_result(self, result):
        print(f"Resultado de los datos: {result}")
        # messagebox.showinfo("Informacion del juego", f"Resultado de los datos: {result}")

    def leave_piece_base(self):
        player = self.players[self.current_player] 
        if player.color == "azul":
            for idx, piece in enumerate(player.pieces):
                if piece.state == Piece.STATE_CAPTURED:
                    piece.state = Piece.STATE_IN_GAME
                    self.board.move_piece(piece, (4, 17 + idx))
                    print(piece.get_actual_pos())
                    return True

        elif player.color == "verde":
            for idx, piece in enumerate(player.pieces):
                if piece.state == Piece.STATE_CAPTURED:
                    piece.state = Piece.STATE_IN_GAME
                    self.board.move_piece(piece, (25, 12 - idx)) 
                    print(piece.get_actual_pos())
                    return True

        elif player.color == "rojo":
            for idx, piece in enumerate(player.pieces):
                if piece.state == Piece.STATE_CAPTURED:
                    piece.state = Piece.STATE_IN_GAME
                    self.board.move_piece(piece, (12 - idx, 4))
                    print(piece.get_actual_pos())
                    return True

        elif player.color == "amarillo":
            for idx, piece in enumerate(player.pieces):
                if piece.state == Piece.STATE_CAPTURED:
                    piece.state = Piece.STATE_IN_GAME
                    self.board.move_piece(piece, (17 + idx, 25))
                    print(piece.get_actual_pos())
                    return True
        return False

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

                piece = board.cells[clicked_row][clicked_col].piece
                piecesIds = [player_piece.pieceId for player_piece in self.players[self.current_player].pieces]

                if board.cells[clicked_row][clicked_col].has_piece() and piece.state == Piece.STATE_IN_GAME and piece.pieceId in piecesIds:
                    piece = board.cells[clicked_row][clicked_col].piece
                    dragger.save_initial(event.pos)
                    dragger.drag_piece(piece)

            elif event.type == pygame.MOUSEMOTION:
                if dragger.dragging:
                    dragger.update_mouse(event.pos)
                    self.render(screen)
                    dragger.update_blit(screen)

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragger.piece != None:
                    board.valid_move(dragger)
                dragger.undrag_piece()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if self.dices_result:
                        print(self.dices_result)

                    if self.check_pair(self.dices_result):
                        is_out_piece = self.leave_piece_base()
                        if not is_out_piece:
                            self.dices_result = []
                        else:
                            Board.plays = []

                    if not self.check_pieces_in_game():
                        Board.plays = [] 
                    self.render(screen)

            elif event.type == pygame.QUIT:
                return False
        
        if not Board.plays:
            if self.dices_result:
                self.next_turn()
            self.roll_dices()
        pygame.display.update()

        return True

    def render(self, screen):
        self.board.render(screen, self.dragger)

