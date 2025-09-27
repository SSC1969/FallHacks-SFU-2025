import pygame

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
GRID_SIZE = 20

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
running = True


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


SCREEN.fill("black")
while running:
    drawGrid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            snapped = snapCoordinates(mouse_x, mouse_y)
            rect = pygame.Rect(snapped[0] - 40, snapped[1] - 40, 80, 80)
            pygame.draw.rect(SCREEN, "blue", rect)

    pygame.display.flip()

    dt = CLOCK.tick(60) / 1000

pygame.quit()
