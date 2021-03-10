import arcade


class Player:
    def __init__(self, name):
        self.name = name
        self.player_list = arcade.SpriteList()
