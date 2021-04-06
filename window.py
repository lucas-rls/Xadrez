import random
import arcade
import math
import os
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
from pprint import pprint


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(CHESSBOARD_SIZE, CHESSBOARD_SIZE, "Jogo de Xadrez - ESII")

        self.player_1 = None
        self.player_2 = None
        self.first_click = None
        self.game_matriz = [[0] * 8 for i in range(8)]

    def setup(self):
        self.player_1 = self.create_player("Lucas", 1)
        self.player_2 = self.create_player("Máquina", 2)

    def on_draw(self):
        arcade.start_render()
        self.render_board()
        self.player_1.player_list.draw()
        self.player_2.player_list.draw()

        self.initialize_matriz(self.player_1.player_list, self.player_2.player_list)

        # Finish the render.
        arcade.finish_render()

    def on_mouse_press(self, x, y, button, modifiers):
        square_x = (
            x / SQUARE_SIZEx + 1 if x % SQUARE_SIZE == 0 else math.ceil(x / SQUARE_SIZE)
        )
        square_y = (
            y / SQUARE_SIZEx + 1 if y % SQUARE_SIZE == 0 else math.ceil(y / SQUARE_SIZE)
        )

        if self.first_click:
            # Recupera a instância da peça no quadrado do primeiro clique
            sprite = self.game_matriz[self.first_click[0] - 1][self.first_click[1] - 1]

            # Checa se o movimento é permitido
            if sprite.check_move(square_x, square_y, self.game_matriz):
                sprite.square_x = square_x
                sprite.square_y = square_y

                self.game_matriz[square_x - 1][square_y - 1] = sprite
                self.game_matriz[self.first_click[0] - 1][
                    self.first_click[1] - 1
                ] = None

                self.first_click = None
            else:
                self.first_click = None
        else:
            if self.game_matriz[square_x - 1][square_y - 1]:
                self.first_click = [square_x, square_y]

    def initialize_matriz(self, p1, p2):
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
        player = Player(name)

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


def main():
    game = GameWindow()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()