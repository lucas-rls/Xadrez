import arcade
from constants import SPRITE_SCALING_PLAYER, SQUARE_SIZE


class AbstractSprite(arcade.Sprite):
    def __init__(self, image, pos_x, pos_y, player, player_number):
        super().__init__(image, SPRITE_SCALING_PLAYER)
        self._square_x = pos_x
        self._square_y = pos_y
        self._player = player
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

    @property
    def player(self):
        return self._player

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
        # Se o o segundo clique não tiver peça returna True senão retorna False
        if not game_matriz[square_x - 1][square_y - 1]:
            return True
        return False

    def check_capture(self, square_x, square_y, game_matriz):
        if (
            game_matriz[square_x - 1][square_y - 1]
            and game_matriz[square_x - 1][square_y - 1].player_number
            != self.player_number
        ):
            return True
        return False


class RookSprite(AbstractSprite):
    def __init__(self, pos_x, pos_y, player, player_number):
        super().__init__(
            "./icons/png/006-rook-dark.png"
            if player_number == 2
            else "./icons/png/006-rook.png",
            pos_x,
            pos_y,
            player,
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
    def __init__(self, pos_x, pos_y, player, player_number):
        super().__init__(
            "./icons/png/010-horse-dark.png"
            if player_number == 2
            else "./icons/png/010-horse.png",
            pos_x,
            pos_y,
            player,
            player_number,
        )

    def check_move(self, square_x, square_y, game_matriz):
        if not super().check_move(square_x, square_y, game_matriz):
            return False

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
    def __init__(self, pos_x, pos_y, player, player_number):
        super().__init__(
            "./icons/png/016-bishop-dark.png"
            if player_number == 2
            else "./icons/png/016-bishop.png",
            pos_x,
            pos_y,
            player,
            player_number,
        )

    def check_move(self, square_x, square_y, game_matriz):
        if not super().check_move(square_x, square_y, game_matriz):
            return False

        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        if abs(xMov) != abs(yMov):
            return False

        indX = self.square_x - 1
        indY = self.square_y - 1
        incX = 1 if xMov > 0 else -1
        incY = 1 if yMov > 0 else -1

        for i in range(0, abs(xMov)):
            indX += incX
            indY += incY
            if game_matriz[indX][indY]:
                return False
        return True


class King(AbstractSprite):
    def __init__(self, pos_x, pos_y, player, player_number):
        super().__init__(
            "./icons/png/009-king-dark.png"
            if player_number == 2
            else "./icons/png/009-king.png",
            pos_x,
            pos_y,
            player,
            player_number,
        )

    def check_move(self, square_x, square_y, game_matriz):
        if not super().check_move(square_x, square_y, game_matriz):
            return False

        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        if abs(xMov) > 1 or abs(yMov) > 1:
            return False

        return True


class Queen(AbstractSprite):
    def __init__(self, pos_x, pos_y, player, player_number):
        super().__init__(
            "./icons/png/007-queen-dark.png"
            if player_number == 2
            else "./icons/png/007-queen.png",
            pos_x,
            pos_y,
            player,
            player_number,
        )

    def check_move(self, square_x, square_y, game_matriz):
        if not super().check_move(square_x, square_y, game_matriz):
            return False

        xMov = square_x - self.square_x
        yMov = square_y - self.square_y

        indX = self.square_x - 1
        indY = self.square_y - 1
        incX = 1 if xMov > 0 else -1
        incY = 1 if yMov > 0 else -1

        if xMov == 0 or yMov == 0:
            variavel = indX if yMov == 0 else indY
            fixo = indY if yMov == 0 else indX
            qtd = xMov if yMov == 0 else yMov
            for i in range(0, qtd, incX if yMov == 0 else incY):
                variavel = variavel + (incX if yMov == 0 else incY)
                hor = variavel if yMov == 0 else fixo
                vert = fixo if yMov == 0 else variavel
                if game_matriz[hor][vert]:
                    return False
            return True

        if abs(xMov) == abs(yMov):
            for i in range(0, abs(xMov)):
                indX += incX
                indY += incY
                if game_matriz[indX][indY]:
                    return False
            return True

        return False


class Pawn(AbstractSprite):
    def __init__(self, pos_x, pos_y, player, player_number):
        super().__init__(
            "./icons/png/008-pawn-dark.png"
            if player_number == 2
            else "./icons/png/008-pawn.png",
            pos_x,
            pos_y,
            player,
            player_number,
        )
        self._first_round = True

    def check_move(self, square_x, square_y, game_matriz):
        if not super().check_move(square_x, square_y, game_matriz):
            if super().check_capture(square_x, square_y, game_matriz):
                return self.check_capture(square_x, square_y, game_matriz)

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

        self._first_round = False
        return True

    def check_capture(self, square_x, square_y, game_matriz):
        y_diff = (
            [square_y, self.square_y]
            if self.player_number == 1
            else [self.square_y, square_y]
        )

        opponent_sprint = game_matriz[square_x - 1][square_y - 1]
        opponent_player = game_matriz[square_x - 1][square_y - 1].player

        if y_diff[0] - y_diff[1] == 1 and abs(square_x - self.square_x) == 1:
            opponent_player.player_list.remove(opponent_sprint)
            return True
        return False
