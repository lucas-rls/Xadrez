import arcade
from constants import (
    WINDOW_SIZE,
    CHESSBOARD_SIZE,
    SQUARE_SIZE,
    SPRITE_SCALING_PLAYER,
    BORDER_MARGIN,
)


class AbstractSprite(arcade.Sprite):
    def __init__(self, image, pos_x, pos_y, player_number):
        super().__init__(image, SPRITE_SCALING_PLAYER)
        self._square_x = pos_x
        self._square_y = pos_y
        self._player_number = player_number
        self.center_x = SQUARE_SIZE * pos_x - SQUARE_SIZE / 2 + BORDER_MARGIN
        self.center_y = SQUARE_SIZE * pos_y - SQUARE_SIZE / 2 + BORDER_MARGIN

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
        self.center_x = SQUARE_SIZE * pos_x - SQUARE_SIZE / 2 + BORDER_MARGIN

    @square_y.setter
    def square_y(self, pos_y):
        self._square_y = pos_y
        self.center_y = SQUARE_SIZE * pos_y - SQUARE_SIZE / 2 + BORDER_MARGIN

    @player_number.setter
    def player_number(self, player_number):
        self._player_number = player_number

    def check_capture(self, square_x, square_y, game_matriz):
        square = game_matriz[square_x - 1][square_y - 1]
        if square:
            if square._player_number != self._player_number:
                return True
        return False

    def detect_horizontal_collision(self, square_x, game_matriz):
        # percorre as casas entre a peca e o destino
        xMov = square_x - self.square_x

        # cria uma var chamada indice, que eh a exata posicao da peca no tabuleiro
        indX = self.square_x - 1

        # define o incremento
        incX = 1 if xMov > 0 else -1

        for i in range(1, abs(xMov)):
            indX += incX
            if game_matriz[indX][self.square_y - 1]:
                return True
        return False

    def detect_vertical_collision(self, square_y, game_matriz):
        # percorre as casas entre a peca e o destino
        yMov = square_y - self.square_y

        # cria uma var chamada indice, que eh a exata posicao da peca no tabuleiro
        indY = self.square_y - 1

        # define o incremento
        incY = 1 if yMov > 0 else -1

        for i in range(1, abs(yMov)):
            indY += incY
            if game_matriz[self.square_x - 1][indY]:
                return True
        return False

    def detect_diagonal_collision(self, square_x, square_y, game_matriz):
        # percorre as casas entre a peca e o destino
        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        # cria uma var chamada indice, que eh a exata posicao da peca no tabuleiro
        indX = self.square_x - 1
        indY = self.square_y - 1

        # define o incremento
        incX = 1 if xMov > 0 else -1
        incY = 1 if yMov > 0 else -1

        # percorre as casas entre a peca e o destino
        for i in range(1, abs(xMov)):
            indY += incY
            indX += incX
            if game_matriz[indX][indY]:
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
        self._first_round = True

    def check_move(self, square_x, square_y, game_matriz):

        # verifica a quantidade de movimento em cada direcao
        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        # se se moveu apenas da direcao vertical, detecta a colisao vertical
        if xMov == 0:
            if not super().detect_vertical_collision(square_y, game_matriz):
                self._first_round = False
                return True
        # se se moveu apenas da direcao horizontal, detecta a colisao horizontal
        elif yMov == 0:
            if not super().detect_horizontal_collision(square_x, game_matriz):
                self._first_round = False
                return True
        return False


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

    def check_move(self, square_x, square_y, game_matriz):
        # Se apenas de movimentar em um dos eixos
        if (square_x - self.square_x != 0 and square_y - self.square_y == 0) or (
            square_x - self.square_x == 0 and square_y - self.square_y != 0
        ):
            return False

        # Se o número de casas andadas for diferente de 3
        if (abs(square_x - self.square_x) + abs(square_y - self.square_y)) != 3:
            return False

        return True


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

    def check_move(self, square_x, square_y, game_matriz):
        # verifica o numero de casas andadas nos eixos
        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        if abs(xMov) != abs(yMov):
            return False

        return not super().detect_diagonal_collision(square_x, square_y, game_matriz)


class King(AbstractSprite):
    def __init__(self, pos_x, pos_y, player_number):
        is_in_check = False
        super().__init__(
            "./icons/png/009-king-dark.png"
            if player_number == 2
            else "./icons/png/009-king.png",
            pos_x,
            pos_y,
            player_number,
        )
        self._first_round = True
        self.is_in_check = False

    def check_move(self, square_x, square_y, game_matriz):
        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        if abs(xMov) == 2 and yMov == 0 and self._first_round:
            rook = (
                game_matriz[0][self.square_y - 1]
                if xMov < 0
                else game_matriz[7][self.square_y - 1]
            )
            rook_mov = 2 if xMov < 0 else -3
            if rook.__class__.__name__ == "RookSprite":
                if rook._first_round:
                    if not super().detect_horizontal_collision(square_x, game_matriz):
                        rook.square_x = rook.square_x + rook_mov
                        self._first_round = False
                        return True
            else:
                rook = game_matriz[0][self.square_y]

        if abs(xMov) > 1 or abs(yMov) > 1:
            return False
        self._first_round = False
        return True


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

    def check_move(self, square_x, square_y, game_matriz):
        # verifica a quantidade de movimento em cada direcao
        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        # se se moveu apenas da direcao vertical, detecta a colisao vertical
        if xMov == 0:
            if not super().detect_vertical_collision(square_y, game_matriz):
                return True
        # se se moveu apenas da direcao horizontal, detecta a colisao horizontal
        elif yMov == 0:
            if not super().detect_horizontal_collision(square_x, game_matriz):
                return True
        # se se moveu diagonalmente, detecta a colisao diagonal
        elif abs(xMov) == abs(yMov):
            return not super().detect_diagonal_collision(
                square_x, square_y, game_matriz
            )
        return False


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
        self._initial_y = pos_y
        self._first_round = True
        self.en_passant_risk = False

    def check_move(self, square_x, square_y, game_matriz):
        if self._first_round and self._initial_y != self.square_y:
            self._first_round = False

        xMov = (
            square_x - self.square_x
        )  # if self._player_number == 1 else square_x - self.square_x
        yMov = (
            square_y - self.square_y
        )  # if self._player_number == 1 else square_y - self.square_y

        if abs(xMov) == 1 and abs(yMov) == 1:
            if (self.player_number == 1 and square_y == 6) or (
                self.player_number == 2 and square_y == 3
            ):
                if not game_matriz[square_x - 1][square_y - 1]:
                    candidate = game_matriz[square_x - 1][self.square_y - 1]
                    if candidate:
                        if candidate.__class__.__name__ == "Pawn":
                            if candidate.en_passant_risk:
                                candidate.square_y = square_y
                                game_matriz[square_x - 1][square_y - 1] = candidate

        capture_mov = super().check_capture(square_x, square_y, game_matriz)

        if capture_mov:
            if abs(xMov) == 1 and abs(yMov) == 1:
                return True
            elif xMov == 0:
                return False

        # Cria lista para saber a ordem da subtração na condição dependendo do jogador
        y_diff = (
            [square_y, self.square_y]
            if self.player_number == 1
            else [self.square_y, square_y]
        )

        # Se o movimento for no eixo x
        # Ou se estiver andando para trás
        # Ou se tiver uma peça no meio do caminho no primeiro movimento
        # Ou se não for a primeira rodada e estiver andando mais que uma casa
        if (square_x - self.square_x != 0) or (
            y_diff[0] - y_diff[1] <= 0
            or (
                self._first_round
                and y_diff[0] - y_diff[1] == 2
                and game_matriz[square_x - 1][
                    int(self.square_y + (square_y - self.square_y) / 2) - 1
                ]
            )
            or (y_diff[0] - y_diff[1] > 1 and not self._first_round)
            or y_diff[0] - y_diff[1] > 2
        ):
            return False

        if self._first_round and abs(square_y - self.square_y) == 2:
            self.en_passant_risk = True
        else:
            self.en_passant_risk = False

        return True
