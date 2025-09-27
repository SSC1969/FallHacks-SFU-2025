import pygame

# Initialization of display

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Game scene

CLOCK = pygame.time.Clock()

# Player

player_x, player_y = 0, 0

PLAYER_COLOUR = (255, 0, 128)

# Process

SCREEN.fill((25, 25, 25))
GRID_BORDER = (200, 200, 200)