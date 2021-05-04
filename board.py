import arcade
from constants import (
    WINDOW_SIZE,
    CHESSBOARD_SIZE,
    SQUARE_SIZE,
    LEFT_MARGIN,
    BOTTOM_MARGIN,
    BRIGHTER_SQUARE,
    DARKER_SQUARE,
    BORDER_MARGIN,
)
from player import Player
from sprites import Rook, Horse, Bishop, King, Queen, Pawn
import math
from arcade import color
from buttons import MyFlatButton
from arcade.gui import UIManager
from help_view import InstructionView
from ia import minimax
import threading
from copy import deepcopy
from os import sys


class Board(object):
    def __init__(self):
        super().__init__()
        self.player_1 = Player("Lucas", 1)
        self.player_2 = Player("Máquina", 2)
        self.game_matriz = [[0] * 8 for i in range(8)]

        self.turn = 1
        self.active_player = 1
        self.waiting_player = 2
        self.selected_sprite = None

        self.last_moves = []

        self.weights = {"King": 900, "Queen": 90, "Rook": 50, "Bishop": 30, "Horse": 30, "Pawn": 10}
        self.player1_score = 1290
        self.player2_score = 1290

        self.initialize_matriz()

    def initialize_matriz(self):
        p1 = self.get_active_player().player_list
        p2 = self.get_waiting_player().player_list
        for i in range(8):
            for j in range(8):
                self.game_matriz[i][j] = 0
        for sprite in p1:
            self.game_matriz[sprite.square_x - 1][sprite.square_y - 1] = sprite
        for sprite in p2:
            self.game_matriz[sprite.square_x - 1][sprite.square_y - 1] = sprite

    def get_player(self, number):
        if number == 1:
            return self.player_1
        return self.player_2

    def get_active_player(self):
        return self.get_player(self.active_player)

    def get_waiting_player(self):
        return self.get_player(self.waiting_player)

    def determine_move(self):
        best_move = minimax(deepcopy(self), 3, True, 2)[0]
        for sprite in self.get_active_player().player_list:
            if sprite.square_x == best_move[0].square_x and sprite.square_y == best_move[0].square_y:
                best_move[0] = sprite

        self.selected_sprite = best_move[0]
        self.move_and_verify_check(best_move[1], best_move[2], self.game_matriz[best_move[1]-1][best_move[2]-1])
        self.change_turn()

        # Fecha thread depois de descobrir o movimento
        sys.exit()


    # funcao que muda o turno
    def change_turn(self):
        print("+==========MUDOU O TURNO===============\n VEZ DE:", self.waiting_player)
        temp = self.active_player
        # troca o player ativo e o que esta aguardando
        self.active_player = self.waiting_player
        self.waiting_player = temp
        # incrementa o turno
        self.turn += 1
        # limpa a selecao
        self.selected_sprite = None

        if self.active_player == 2:
            # Abre uma thread para descobrir o movimento
            t = threading.Thread(target=self.determine_move)
            t.start()

    # funcao de promocao do peao (ainda precisa ser alterada para pegar uma peca do cemiterio)
    def promote_pawn(self, pawn_sprite, active_player):
        # pega o player atual
        pl = self.get_active_player()
        # substitui seu peao por uma rainha
        pl.player_list.append(
            Queen(pawn_sprite.square_x, pawn_sprite.square_y, pl.player_number)
        )
        # remove o peao da lista de sprites
        pl.player_list.remove(pawn_sprite)

    # funcao que verifica o check de um rei
    def results_check(self, player_number):
        #print("verificou o check para o player ", player_number)
        # pl = o jogador que tem o rei que sera testado
        pl = self.get_player(player_number)

        # pl_2 = o jogador adversario do pl
        pl_2 = (
            self.get_active_player()
            if player_number == self.waiting_player
            else self.get_waiting_player()
        )

        # atualiza a matriz antes de verificar
        self.initialize_matriz()

        # pega o rei do pl
        king = pl.get_king()

        # se existir um rei (protecao)
        if king:
            # verifica, para cada um dos adversarios, se o rei tem o risco de ser capturado
            for sprite in pl_2.player_list:
                if sprite.check_move(king.square_x, king.square_y, self.game_matriz):
                    print("CHECK")
                    king.is_in_check = True
                    return True
        # retorna false se o rei nao esta em check
        king.is_in_check = False
        return False

    def move(self, square_x, square_y, sprite):
        old_square_x = self.selected_sprite.square_x
        old_square_y = self.selected_sprite.square_y

        if sprite:
            # envia o sprite pro cemiterio do adversario
            self.get_waiting_player().send_to_cemetery(sprite)

            if self.get_waiting_player().player_number == 1:
                self.player1_score -= self.weights[type(sprite).__name__]
            else:
                self.player2_score -= self.weights[type(sprite).__name__]
        
        self.last_moves.append([old_square_x, old_square_y, sprite, self.selected_sprite])

        self.selected_sprite.square_x = square_x
        self.selected_sprite.square_y = square_y

        self.initialize_matriz()

        return True
    
    def undo_move(self):
        sprite = self.last_moves[-1][3]
        sprite.square_x = self.last_moves[-1][0]
        sprite.square_y = self.last_moves[-1][1]
        
        last_move_sprite = self.last_moves[-1][2]

        if last_move_sprite:
            self.get_player(self.waiting_player).cemetery.remove(last_move_sprite)
            self.get_player(self.waiting_player).player_list.append(last_move_sprite)
            self.game_matriz[last_move_sprite.square_x - 1][last_move_sprite.square_y - 1] = last_move_sprite

            if self.get_waiting_player().player_number == 1:
                self.player1_score += self.weights[type(last_move_sprite).__name__]
            else:
                self.player2_score += self.weights[type(last_move_sprite).__name__]
        
        self.last_moves.pop()

        self.initialize_matriz()

        return True

    def move_and_verify_check(self, square_x, square_y, sprite):
        self.move(square_x, square_y, sprite)

        # verifica se o rei do jogador ira ficar em check
        active_player_king_check = self.results_check(self.active_player)
        # se o movimento colocar o rei do jogador em check, nao permite q a jogada seja executada
        if active_player_king_check:
            self.undo_move()
            self.get_active_player().change_king_check_status(False)
            print("voltou o movimento por colocar o rei em check")
            #self.results_check(self.waiting_player)
            return False
        return True
    
    def click(self, square_x, square_y):
        # Recupera a instância da peça no quadrado do primeiro clique
        sprite = self.game_matriz[square_x - 1][square_y - 1]

        # se clicou em um lugar que tenha um sprite...
        if sprite:
            # caso o sprite seja do jogador, seleciona o sprite clicado
            if sprite._player_number == self.active_player:
                self.selected_sprite = sprite
            # caso seja um sprite do adversario e ha um sprite selecionado
            elif self.selected_sprite:
                # testa o movimento pra aquele lugar...
                if self.selected_sprite.check_move(
                    square_x, square_y, self.game_matriz
                ):
                    # chama a verificacao do check e realiza o movimento se tudo esta ok
                    if self.move_and_verify_check(square_x, square_y, sprite):
                        # verifica se o rei do adversario ficara em check e atualiza o status do rei adversario
                        self.results_check(self.waiting_player)
                        self.change_turn()

                    

        else:
            if self.selected_sprite:
                if self.selected_sprite.check_move(
                    square_x, square_y, self.game_matriz
                ):
                    # trata condicao do en passant
                    if (
                        self.selected_sprite.__class__.__name__ == "Pawn"
                        and square_y == 3
                        or square_y == 6
                    ):
                        sprite = self.game_matriz[square_x - 1][square_y - 1]
                        if sprite:
                            self.get_waiting_player().send_to_cemetery(sprite)

                    if self.move_and_verify_check(square_x, square_y, sprite):
                        # checa promocao do peao
                        if self.selected_sprite.__class__.__name__ == "Pawn":
                            if (square_y == 8 and self.active_player == 1) or (
                                square_y == 1 and self.active_player == 2
                            ):
                                self.promote_pawn(
                                    self.selected_sprite, self.active_player
                                )
                        self.results_check(self.waiting_player)
                        self.change_turn()

    def get_moves(self):
        moves = []
        for sprite in self.get_active_player().player_list:
            self.selected_sprite = sprite
            print(self.active_player)
            for i in range(len(self.game_matriz)):
                for j in range(len(self.game_matriz[i])):
                    if (  # Se á peça pode se mover até a desejada posição
                        self.selected_sprite.check_move(i + 1, j + 1, self.game_matriz)
                        and (  # E a nova posição não contém uma peça do mesmo jogador
                            not self.game_matriz[i][j]
                            or self.selected_sprite.player_number
                            != self.game_matriz[i][j].player_number
                        )
                    ):
                        self.move(i+1, j+1, self.game_matriz[i][j])
                        # verifica se o rei do jogador ira ficar em check
                        active_player_king_check = self.results_check(self.active_player)
                        self.get_active_player().change_king_check_status(False)
                        
                        self.undo_move()

                        if not active_player_king_check:
                            moves.append([sprite, i+1, j+1])
        return moves
    
    @staticmethod
    def print_matrix(matrix):
        s = [[(type(e).__name__ if type(e)!=int else "-") for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print("---------------------------------------------------------------------------")
