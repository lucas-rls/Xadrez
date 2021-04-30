import arcade
from sprites import RookSprite, HorseSprite, Bishop, King, Queen, Pawn


class Player:
    def __init__(self, name, player_number):
        self.name = name
        self.player_list = arcade.SpriteList()
        self.cemetery = arcade.SpriteList()
        self.player_number = player_number

        first_row = 1 if player_number == 1 else 8
        second_row = 2 if player_number == 1 else 7

        self.player_list.append(RookSprite(1, first_row, player_number))
        self.player_list.append(HorseSprite(2, first_row, player_number))
        self.player_list.append(Bishop(3, first_row, player_number))
        self.player_list.append(King(4, first_row, player_number))
        self.player_list.append(Queen(5, first_row, player_number))
        self.player_list.append(Bishop(6, first_row, player_number))
        self.player_list.append(HorseSprite(7, first_row, player_number))
        self.player_list.append(RookSprite(8, first_row, player_number))

        self.player_list.append(Pawn(1, second_row, player_number))
        self.player_list.append(Pawn(2, second_row, player_number))
        self.player_list.append(Pawn(3, second_row, player_number))
        self.player_list.append(Pawn(4, second_row, player_number))
        self.player_list.append(Pawn(5, second_row, player_number))
        self.player_list.append(Pawn(6, second_row, player_number))
        self.player_list.append(Pawn(7, second_row, player_number))
        self.player_list.append(Pawn(8, second_row, player_number))

    def send_to_cemetery(self, sprite):
        self.cemetery.append(sprite)
        self.player_list.remove(sprite)

    def get_king(self):
        for sprite in self.player_list:
            if sprite.__class__.__name__ == "King":
                return sprite
        return None

    def change_king_check_status(self, status):
        king = self.get_king()
        king.is_in_check = status
