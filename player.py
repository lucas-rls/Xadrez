import arcade


class Player:
    def __init__(self, name, number):
        self.name = name
        self.player_list = arcade.SpriteList()
        self.cemetery = arcade.SpriteList()
        self.player_number = number

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
