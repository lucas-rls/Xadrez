import arcade
import random
import os
from constants import WINDOW_SIZE
from buttons import MyFlatButton
from arcade.gui import UIManager


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5


class InstructionView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_manager = UIManager()

    def draw_text(self, texts):
        margin = 30
        y_value = WINDOW_SIZE - 55

        for index, text in enumerate(texts):
            is_title = False

            if "*" in text:
                is_title = True
                text = text.replace("*", "", 2)

            lines_qty = text.count("\n")

            y_value -= 30 if is_title else 20 + (lines_qty) * 15

            arcade.draw_text(
                text=text,
                start_x=margin,
                start_y=y_value,
                color=arcade.color.WHITE,
                font_size=18 if is_title else 12,
                width=WINDOW_SIZE - margin,
            )

        button = MyFlatButton(
            text="Próxima página >",
            center_x=WINDOW_SIZE / 2,
            center_y=20,
            width=300,
            actual_view=self,
            next_view=InstructionView2(self.game_view),
        )

        self.ui_manager.add_ui_element(button)

    def on_show(self):
        arcade.set_background_color(arcade.color.BROWN_NOSE)

    def on_draw(self):
        arcade.start_render()

        self.ui_manager.purge_ui_elements()

        texts = [
            "*Definições*",
            "Xeque - Rei sob ameaça de captura.",
            "Xeque-mate - Rei sob ameaça de captura, sem que ele tenha como escapar.",
            "Captura - Determinada peça toma a posição de uma outra peça adversária e esta é removida.",
            "*Movimentação das peças*",
            "Torre - A movimentação da torre se dá somente de forma horizontal (linhas do tabuleiro) ou\n"
            "vertical (colunas do tabuleiro).",
            "Bispo - Esta peça se movimenta somente nas diagonais do tabuleiro.",
            "Dama - Uma dama pode se movimentar tanto na horizontal como na vertical (assim como uma torre)\n"
            "ou nas diagonais (assim como um bispo).",
            "Rei - Se movimenta em qualquer direção mas com limitação quanto ao número de casas. O limite\n"
            "de casas que um rei pode se deslocar é de uma casa por lance. O rei NUNCA pode fazer um\n"
            "movimentoque resulte em um xeque para ele.",
            "Peão - O peão somente pode fazer movimentos adjacentes à sua posição anterior, isto é, não pode\n"
            "retroceder. O peão, assim como o rei só pode deslocar-se 1 casa à frente por lance, no entanto,\n"
            "quando o peão ainda está na sua posição inicial, este pode dar um salto de 2 casas à frente.",
            "Cavalo - É a única peça que pode 'saltar' sobre outras peças. A movimentação do cavalo é feita\n"
            "em forma de 'L', ou seja, anda 2 casas em qualquer direção (vertical ou horizontal) e depois\n"
            "mais uma em sentido perpendicular.",
            "*Movimentos Especiais*",
            "Roque - É um movimento que envolve 2 peças da mesma cor. São elas o Rei e qualquer uma das\n"
            "torres. O roque é feito ao mover o rei 2 casas para qualquer lado na horizontal. Para se\n"
            "fazer um roque é obrigatório satisfazer as seguintes condições:",
            "   - O Rei não pode ter sido mexido até o momento do roque. Tem que estar na posição inicial.",
            "   - Assim como o Rei, a Torre tambem não pode ter sido mexida, portanto deve estar na sua\n"
            "   posição inicial.",
            "   - As casas pelas quais o Rei irá passar, não podem estar sob ameaça das peças adversárias.",
            "   - Não pode haver nenhuma peça obstruindo o caminho onde passarão Rei e Torre.",
            "   - OBS: Para efetuar o Roque, clique sobre o Rei e clique sobre a posição desejada. O sistema\n"
            "   moverá a Torre automaticamente.",
            "Captura en-passant - Esta captura é um tipo especial feita por peões. Regras para a captura\n"
            "en-passant:",
            "   - O peão a ser capturado deve ter feito o lance inicial de 2 casas.",
            "   - O peão que vai fazer a captura, pode fazê-la como se o peão a ser capturado estivesse\n"
            "   exatamente 1 casa à frente da sua posição inicial e deslocado 1 coluna a esquerda ou a\n"
            "   direita como na captura normal.",
            "*Promoção de Peões*",
            "Um peão, ao alcançar a última linha do tabuleiro (no caso das brancas a linha 8, e no caso das\n"
            "pretas a linha 1) é promovido, o jogador é obrigado a escolher entre uma das seguintes peças\n"
            "para substituí-lo:",
            "   Dama    |" "   Torre   |" "   Bispo   |" "   Cavalo  ",
        ]

        self.draw_text(texts)

        button = MyFlatButton(
            text="Voltar ao jogo",
            center_x=WINDOW_SIZE / 2,
            center_y=WINDOW_SIZE - 23,
            width=250,
            actual_view=self,
            next_view=self.game_view,
        )
        self.ui_manager.add_ui_element(button)


class InstructionView2(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.ui_manager = UIManager()

    def draw_text(self, texts):
        margin = 30
        y_value = WINDOW_SIZE - 55

        for index, text in enumerate(texts):
            is_title = False

            if "*" in text:
                is_title = True
                text = text.replace("*", "", 2)

            lines_qty = text.count("\n")

            y_value -= 30 if is_title else 20 + (lines_qty) * 15

            arcade.draw_text(
                text=text,
                start_x=margin,
                start_y=y_value,
                color=arcade.color.WHITE,
                font_size=18 if is_title else 12,
                width=WINDOW_SIZE - margin,
            )

        button = MyFlatButton(
            text="< Página Anterior",
            center_x=WINDOW_SIZE / 2,
            center_y=20,
            width=300,
            actual_view=self,
            next_view=InstructionView(self.game_view),
        )

        self.ui_manager.add_ui_element(button)

    def on_show(self):
        arcade.set_background_color(arcade.color.BROWN_NOSE)

    def on_draw(self):
        arcade.start_render()

        self.ui_manager.purge_ui_elements()

        texts = [
            "*Vitória*",
            "Só existem 2 formas de um jogador vencer. São elas:",
            "Se o jogador fazer um Xeque-Mate ao adversário.",
            "Se o adversário desistir da partida.",
            "*Empates*",
            "Uma partida é considerada empatada quando:",
            "- Um jogador não puder mais efetuar jogadas consideradas legais.",
            "- Um jogador propor o empate e o outro aceitar.",
            "- Os jogadores não tiverem mais peças suficientes para dar xeque-mate ao adversário. É\n"
            "considerado material insuficiente:",
            "   - O Rei e um Bispo",
            "   - O Rei e um Cavalo",
            "   - O Rei e dois Cavalos contra um Rei sozinho",
        ]

        self.draw_text(texts)

        button = MyFlatButton(
            text="Voltar ao jogo",
            center_x=WINDOW_SIZE / 2,
            center_y=WINDOW_SIZE - 23,
            width=250,
            actual_view=self,
            next_view=self.game_view,
        )
        self.ui_manager.add_ui_element(button)
