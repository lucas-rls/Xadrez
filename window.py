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
from sprites import RookSprite, HorseSprite, Bishop, King, Queen, Pawn
import math
from arcade import color
from buttons import MyFlatButton
from arcade.gui import UIManager
from help_view import InstructionView
from board import Board


class GameWindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.board = Board()

        self.ui_manager = UIManager()

    def on_show(self):
        self.ui_manager.purge_ui_elements()
        button = MyFlatButton(
            text="Ajuda",
            center_x=WINDOW_SIZE / 2,
            center_y=WINDOW_SIZE - 23,
            width=250,
            actual_view=self,
            next_view=InstructionView(self),
        )
        self.ui_manager.add_ui_element(button)
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.render_board()
        self.board.player_1.player_list.draw()
        self.board.player_2.player_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if (
            x >= BORDER_MARGIN
            and x <= CHESSBOARD_SIZE + BORDER_MARGIN
            and y >= BORDER_MARGIN
            and y <= CHESSBOARD_SIZE
        ):
            x = x - BORDER_MARGIN
            y = y - BORDER_MARGIN

            square_x = (
                x / SQUARE_SIZE + 1
                if x % SQUARE_SIZE == 0
                else math.ceil(x / SQUARE_SIZE)
            )
            square_y = (
                y / SQUARE_SIZE + 1
                if y % SQUARE_SIZE == 0
                else math.ceil(y / SQUARE_SIZE)
            )

            self.board.click(square_x, square_y)
            
    def render_board(self):
        flag = False

        for row in range(8):
            for column in range(8):
                x = column * SQUARE_SIZE + LEFT_MARGIN + BORDER_MARGIN
                y = row * SQUARE_SIZE + BOTTOM_MARGIN + BORDER_MARGIN

                # Desenha quadrado
                arcade.draw_rectangle_filled(
                    x,
                    y,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                    BRIGHTER_SQUARE if flag else DARKER_SQUARE,
                )

                flag = not flag
            flag = not flag

        if self.board.selected_sprite:
            # Se existe um sprite selecionado colore fundo
            arcade.draw_rectangle_filled(
                (self.board.selected_sprite.square_x - 1) * SQUARE_SIZE
                + LEFT_MARGIN
                + BORDER_MARGIN,
                (self.board.selected_sprite.square_y - 1) * SQUARE_SIZE
                + BOTTOM_MARGIN
                + BORDER_MARGIN,
                SQUARE_SIZE,
                SQUARE_SIZE,
                (255, 191, 0),
            )

            for i in range(len(self.board.game_matriz)):
                for j in range(len(self.board.game_matriz[i])):
                    if (  # Se á peça pode se mover até a desejada posição
                        self.board.selected_sprite.check_move(i + 1, j + 1, self.board.game_matriz)
                        and (  # E a nova posição não contém uma peça do mesmo jogador
                            not self.board.game_matriz[i][j]
                            or self.board.selected_sprite.player_number
                            != self.board.game_matriz[i][j].player_number
                        )
                    ):
                        self.board.move(i+1, j+1, self.board.game_matriz[i][j])
                        # verifica se o rei do jogador ira ficar em check
                        active_player_king_check = self.board.results_check(self.board.active_player)
                        self.board.get_active_player().change_king_check_status(False)
                        
                        self.board.undo_move()

                        if not active_player_king_check:
                            arcade.draw_rectangle_filled(
                                (i) * SQUARE_SIZE + LEFT_MARGIN + BORDER_MARGIN,
                                (j) * SQUARE_SIZE + BOTTOM_MARGIN + BORDER_MARGIN,
                                SQUARE_SIZE,
                                SQUARE_SIZE,
                                (0, 127, 255, 200),
                            )



def main():
    window = arcade.Window(WINDOW_SIZE, WINDOW_SIZE, "Jogo de Xadrez - ESII")
    game = GameWindow()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
