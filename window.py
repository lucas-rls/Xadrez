import arcade
from constants import (
    CHESSBOARD_SIZE,
    SQUARE_SIZE,
    LEFT_MARGIN,
    BOTTOM_MARGIN,
    BRIGHTER_SQUARE,
    DARKER_SQUARE,
)
from player import Player
from sprites import RookSprite, HorseSprite, Bishop, King, Queen, Pawn
import math


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(CHESSBOARD_SIZE, CHESSBOARD_SIZE, "Jogo de Xadrez - ESII")

        self.player_1 = None
        self.player_2 = None
        #       self.first_click = None
        self.game_matriz = [[0] * 8 for i in range(8)]

        self.turn = 1
        self.active_player = 1
        self.waiting_player = 2
        self.selected_sprite = None

    def setup(self):
        self.player_1 = self.create_player("Lucas", 1)
        self.player_2 = self.create_player("Máquina", 2)

    def on_draw(self):
        arcade.start_render()
        self.render_board()
        self.player_1.player_list.draw()
        self.player_2.player_list.draw()

        self.initialize_matriz()

        # Finish the render.
        arcade.finish_render()

    def on_mouse_press(self, x, y, button, modifiers):
        square_x = (
            x / SQUARE_SIZEx + 1 if x % SQUARE_SIZE == 0 else math.ceil(x / SQUARE_SIZE)
        )
        square_y = (
            y / SQUARE_SIZEx + 1 if y % SQUARE_SIZE == 0 else math.ceil(y / SQUARE_SIZE)
        )

        # Recupera a instância da peça no quadrado do primeiro clique
        sprite = self.game_matriz[square_x - 1][square_y - 1]

        #se clicou em um lugar que tenha um sprite...
        if sprite:
            #caso o sprite seja do jogador, seleciona o sprite clicado
            if sprite._player_number == self.active_player:
                self.selected_sprite = sprite
            #caso seja um sprite do adversario
            else:
                #se ha um sprite selecionado...
                if self.selected_sprite:
                    #testa o movimento pra aquele lugar...
                    if self.selected_sprite.check_move(square_x, square_y, self.game_matriz):
                        #se o movimento eh valido....
                        #envia o sprite pro cemiterio do adversario
                        self.get_waiting_player().send_to_cemetery(sprite)

                        # chama a verificacao do check e realiza o movimento se tudo esta ok
                        if self.move_and_verify_check(square_x, square_y, sprite):
                            # verifica se o rei do adversario ficara em check e atualiza o status do rei adversario
                            self.results_check(self.waiting_player)
                            self.change_turn()

        else:
            if self.selected_sprite:
                if self.selected_sprite.check_move(square_x, square_y, self.game_matriz):
                    if self.move_and_verify_check(square_x, square_y, sprite):
                        #checa promocao do peao
                        if self.selected_sprite.__class__.__name__ == "Pawn":
                            if (square_y == 8 and self.active_player == 1) or (square_y == 1 and self.active_player == 2):
                                self.promote_pawn(self.selected_sprite, self.active_player)
                        self.results_check(self.waiting_player)
                        self.change_turn()

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

    @staticmethod
    def render_board():
        flag = False

        # Loop for each row
        for row in range(8):
            # Loop for each column
            for column in range(8):
                # Calculate our location
                x = column * SQUARE_SIZE + LEFT_MARGIN
                y = row * SQUARE_SIZE + BOTTOM_MARGIN

                # Draw the item
                arcade.draw_rectangle_filled(
                    x,
                    y,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                    BRIGHTER_SQUARE if flag else DARKER_SQUARE,
                )

                flag = not flag
            flag = not flag

    @staticmethod
    def create_player(name, player_number):
        player = Player(name, player_number)
        first_row = 1 if player_number == 1 else 8
        second_row = 2 if player_number == 1 else 7

        player.player_list.append(RookSprite(1, first_row, player_number))
        player.player_list.append(HorseSprite(2, first_row, player_number))
        player.player_list.append(Bishop(3, first_row, player_number))
        player.player_list.append(King(4, first_row, player_number))
        player.player_list.append(Queen(5, first_row, player_number))
        player.player_list.append(Bishop(6, first_row, player_number))
        player.player_list.append(HorseSprite(7, first_row, player_number))
        player.player_list.append(RookSprite(8, first_row, player_number))

        player.player_list.append(Pawn(1, second_row, player_number))
        player.player_list.append(Pawn(2, second_row, player_number))
        player.player_list.append(Pawn(3, second_row, player_number))
        player.player_list.append(Pawn(4, second_row, player_number))
        player.player_list.append(Pawn(5, second_row, player_number))
        player.player_list.append(Pawn(6, second_row, player_number))
        player.player_list.append(Pawn(7, second_row, player_number))
        player.player_list.append(Pawn(8, second_row, player_number))

        return player

    def get_player(self, number):
        if number == 1:
            return self.player_1
        return self.player_2

    def get_active_player(self):
        return self.get_player(self.active_player)

    def get_waiting_player(self):
        return self.get_player(self.waiting_player)

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

    # funcao de promocao do peao (ainda precisa ser alterada para pegar uma peca do cemiterio)
    def promote_pawn(self, pawn_sprite, active_player):
        # pega o player atual
        pl = self.get_active_player()
        # substitui seu peao por uma rainha
        pl.player_list.append(Queen(pawn_sprite.square_x, pawn_sprite.square_y, pl.player_number))
        # remove o peao da lista de sprites
        pl.player_list.remove(pawn_sprite)

    # funcao que verifica o check de um rei
    def results_check(self, player_number):
        print("verificou o check para o player ", player_number)
        # pl = o jogador que tem o rei que sera testado
        pl = self.get_player(player_number)

        # pl_2 = o jogador adversario do pl
        pl_2 = self.get_active_player() if player_number == self.waiting_player else self.get_waiting_player()

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
                    # muda o status do rei para "em check"
                    king.is_in_check = True
                    return True
                # se o rei nao esta mais em check, reseta a flag de check
                king.is_in_check = False

        # retorna false se o rei nao esta em check
        return False

    def move_and_verify_check(self, square_x, square_y, sprite):
        # salva a posicao anterior em caso de aborto do movimento por check
        old_square_x = self.selected_sprite.square_x
        old_square_y = self.selected_sprite.square_y

        # realiza o movimento
        self.selected_sprite.square_x = square_x
        self.selected_sprite.square_y = square_y

        self.initialize_matriz()

        # verifica se o rei do jogador ira ficar em check
        active_player_king_check = self.results_check(self.active_player)
        # se o movimento colocar o rei do jogador em check, nao permite q a jogada seja executada
        if active_player_king_check:
            if (sprite):
                self.game_matriz[square_x - 1][square_y - 1] = sprite
                self.get_player(self.waiting_player).cemetery.remove(sprite)
            self.selected_sprite.square_x = old_square_x
            self.selected_sprite.square_y = old_square_y
            print("voltou o movimento por colocar o rei em check")
            self.results_check(self.waiting_player)
            return False
        return True


def main():
    game = GameWindow()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
