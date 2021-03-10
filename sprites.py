import arcade
from constants import SPRITE_SCALING_PLAYER, SQUARE_SIZE


class AbstractSprite(arcade.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(image, SPRITE_SCALING_PLAYER)
        self._square_x = pos_x
        self._square_y = pos_y
        self.center_x = SQUARE_SIZE * pos_x - SQUARE_SIZE / 2
        self.center_y = SQUARE_SIZE * pos_y - SQUARE_SIZE / 2

    @property
    def square_x(self):
        return self._square_x

    @property
    def square_y(self):
        return self._square_y

    @square_x.setter
    def square_x(self, pos_x):
        self._square_x = pos_x
        self.center_x = SQUARE_SIZE * pos_x - SQUARE_SIZE / 2

    @square_y.setter
    def square_y(self, pos_y):
        self._square_y = pos_y
        self.center_y = SQUARE_SIZE * pos_y - SQUARE_SIZE / 2


class RookSprite(AbstractSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__("./icons/png/006-rook.png", pos_x, pos_y)


class HorseSprite(AbstractSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__("./icons/png/010-horse.png", pos_x, pos_y)


class Bishop(AbstractSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__("./icons/png/016-bishop.png", pos_x, pos_y)


class King(AbstractSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__("./icons/png/009-king.png", pos_x, pos_y)


class Queen(AbstractSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__("./icons/png/007-queen.png", pos_x, pos_y)


class Pawn(AbstractSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__("./icons/png/008-pawn.png", pos_x, pos_y)
