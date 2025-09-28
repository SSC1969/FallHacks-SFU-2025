from config import player_x, player_y, PLAYER_COLOUR
from draw_logic import LEVEL1
# 
import os

# uses sprite stuff ?? 
class player(pygame.sprite.Sprite):
    player_x = 0
    player_y = 0

    # has file of images to circle through
    def __init__(self, player_x, player_y, images):
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

    def collisionCheckWall(self):
        tile = LEVEL1[self.player_y][self.player_x]
        if (tile == 2): # This means it hit a wall
            return False
        
    def collisionCheckWall(self):
        tile = LEVEL1[self.player_y][self.player_x]
        if (tile == 3): # This means it hit a wall
            return True
