import pygame

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
GRID_SIZE = 20

pygame.init()


def drawGrid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(SCREEN, "white", rect, 1)


def snapCoordinates(x, y):
    factor_x = round(x / GRID_SIZE)
    factor_y = round(y / GRID_SIZE)

    factor_x *= GRID_SIZE
    factor_y *= GRID_SIZE

    return (factor_x, factor_y)
