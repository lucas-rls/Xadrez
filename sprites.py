import arcade
from constants import SPRITE_SCALING_PLAYER, SQUARE_SIZE


class AbstractSprite(arcade.Sprite):
    def __init__(self, image, pos_x, pos_y, player_number):
        super().__init__(image, SPRITE_SCALING_PLAYER)
        self._square_x = pos_x
        self._square_y = pos_y
        self._player_number = player_number
        self.center_x = SQUARE_SIZE * pos_x - SQUARE_SIZE / 2
        self.center_y = SQUARE_SIZE * pos_y - SQUARE_SIZE / 2

    @property
    def square_x(self):
        return self._square_x

    @property
    def square_y(self):
        return self._square_y

    @property
    def player_number(self):
        return self._player_number

    @square_x.setter
    def square_x(self, pos_x):
        self._square_x = pos_x
        self.center_x = SQUARE_SIZE * pos_x - SQUARE_SIZE / 2

    @square_y.setter
    def square_y(self, pos_y):
        self._square_y = pos_y
        self.center_y = SQUARE_SIZE * pos_y - SQUARE_SIZE / 2

    @player_number.setter
    def player_number(self, player_number):
        self._player_number = player_number

    def check_move(self, square_x, square_y, game_matriz):
        # Se o o segundo clique não tiver peça return True senão retorna False
        if not game_matriz[square_x - 1][square_y - 1]:
            return True
        return False


class RookSprite(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        super().__init__(
            "./icons/png/006-rook-dark.png"
            if player_number == 2
            else "./icons/png/006-rook.png",
            pos_x,
            pos_y,
            player_number,
        )

    def check_move(self, square_x, square_y, game_matriz):
        if not super().check_move(square_x, square_y, game_matriz):
            return False

        # Se o movimento não for em apenas um eixo retorna False
        if (square_x - self.square_x != 0 and square_y - self.square_y != 0) or (
            square_y - self.square_y == 0 and square_x - self.square_x == 0
        ):
            return False

        # Checa em qual eixo ocorreu o movimento
        if square_x - self.square_x != 0:
            is_x = True
            exis = [square_x, self.square_x]
        else:
            is_x = False
            exis = [square_y, self.square_y]

        # Ordena a lista
        if exis[1] < exis[0]:
            exis.append(exis.pop(0))

        # Checa se existe alguém no meio do caminho do movimento
        for i in range(exis[0], exis[1] - 1):
            if game_matriz[i if is_x else self.square_x - 1][
                self.square_y - 1 if is_x else i
            ]:
                return False

        return True


class HorseSprite(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        super().__init__(
            "./icons/png/010-horse-dark.png"
            if player_number == 2
            else "./icons/png/010-horse.png",
            pos_x,
            pos_y,
            player_number,
        )


class Bishop(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        super().__init__(
            "./icons/png/016-bishop-dark.png"
            if player_number == 2
            else "./icons/png/016-bishop.png",
            pos_x,
            pos_y,
            player_number,
        )


class King(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        super().__init__(
            "./icons/png/009-king-dark.png"
            if player_number == 2
            else "./icons/png/009-king.png",
            pos_x,
            pos_y,
            player_number,
        )


class Queen(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        super().__init__(
            "./icons/png/007-queen-dark.png"
            if player_number == 2
            else "./icons/png/007-queen.png",
            pos_x,
            pos_y,
            player_number,
        )


class Pawn(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        super().__init__(
            "./icons/png/008-pawn-dark.png"
            if player_number == 2
            else "./icons/png/008-pawn.png",
            pos_x,
            pos_y,
            player_number,
        )
