from config import player_x, player_y, PLAYER_COLOUR
from draw_logic import LEVEL1
import pygame

class player(pygame.sprite.Sprite):
    player_x = 0
    player_y = 0

    width = 50
    height = 50
    SURFACE_COLOUR = (167, 255, 100)
    COLOUR = (255, 100, 98)

    def __init__(self, player_x, player_y):
        super().__init__()

        sheet = pygame.image.load("assets/player.png").convert_alpha()
        
        # Define area for frame

        frame_rect = pygame.Rect(0, 0, self.width, self.height)
        # e.g. top-left tile; move the rect to pick the sprite used in the spritesheet

        # "Cut out" the frame
        self.image = sheet.subsurface(frame_rect).copy()

        # Position the sprite
        self.rect = self.image.get_rect(topleft=(player_x, player_y))

        self.player_x = player_x
        self.player_y = player_y



    def moveUp(self):
        self.player_y += 1

    def moveLeft(self):
        self.player_x -= 1

    def moveRight(self):
        self.player_x += 1

    def moveDown(self):
        self.player_y -= 1

    def collisionCheckWall(self):
        tile = LEVEL1[self.player_y][self.player_x]
        if (tile == 2): # This means it hit a wall
            return False
        
    def collisionCheckWall(self):
        tile = LEVEL1[self.player_y][self.player_x]
        if (tile == 3): # This means it hit a wall
            return True