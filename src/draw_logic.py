import pygame

# Screen
from game import WINDOW_HEIGHT, WINDOW_WIDTH

# Level

COLOURS = {
    0: (30, 50, 200),  # Water
    1: (100, 100, 100),  # Ground
    2: (0, 128, 128),  # Wall
}

LEVEL1 = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 2, 1],
    [0, 2, 2, 1, 1, 1, 1, 0, 1, 1, 2, 2],
    [0, 0, 2, 1, 1, 1, 1, 0, 0, 1, 2, 2],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
]

ROWS = len(LEVEL1)
COLS = len(LEVEL1[0])
TILE_SIZE = min(WINDOW_WIDTH // COLS, WINDOW_HEIGHT // ROWS)


def drawGrid(screen, border):
    for y in range(ROWS):
        for x in range(COLS):
            tile = LEVEL1[y][x]
            colour = COLOURS[tile]
            background_tile = pygame.Rect(
                x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(screen, colour, background_tile)

    # Draw vertical grid lines
    for x in range(0, WINDOW_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, border, (x, 0), (x, WINDOW_HEIGHT))
    # Draw horizontal grid lines
    for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, border, (0, y), (WINDOW_WIDTH, y))


def drawPlayer(player_x, player_y):
    player_rect = pygame.Rect(
        player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE
    )
    pygame.draw.rect(SCREEN, PLAYER_COLOUR, player_rect)


def snapCoordinates(x, y):
    factor_x = round(x / TILE_SIZE)
    factor_y = round(y / TILE_SIZE)

    factor_x *= TILE_SIZE
    factor_y *= TILE_SIZE

    return (factor_x, factor_y)


def pixel_to_grid(px, py):
    return px // TILE_SIZE, py // TILE_SIZE
