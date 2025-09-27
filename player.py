from config import player_x, player_y, PLAYER_COLOUR
from draw_logic import LEVEL1

class player:
    player_x = 0
    player_y = 0

    def __init__(self, player_x, player_y):
        self.player_x = player_x
        self.player_y = player_y

    def moveUp(self):
        self.player_y += 1

    def moveLeft(self):
        self.player_x -= 1

    def moveRight(self):
        self.player.x += 1

    def moveLeft(self):
        self.player.x -= 1

    def collisionCheck(self):
        tile = 
        if (player_x, player_y == )