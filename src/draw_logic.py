import pygame

# self.screen
# Level


class DrawLogic:
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
    rows: int
    cols: int
    tile_size: int
    screen: object
    player_colour: object
    WINDOW_WIDTH: int
    WINDOW_HEIGHT: int

    def __init__(self, screen, window_size, border, player_colour):
        self.rows = len(self.LEVEL1)
        self.cols = len(self.LEVEL1[0])
        self.screen = screen
        self.WINDOW_WIDTH = window_size[0]
        self.WINDOW_HEIGHT = window_size[1]
        self.player_colour = player_colour
        self.tile_size = min(
            self.WINDOW_WIDTH // self.cols, self.WINDOW_HEIGHT // self.rows
        )

    def drawGrid(self):
        for y in range(self.rows):
            for x in range(self.cols):
                tile = self.LEVEL1[y][x]
                colour = self.COLOURS[tile]
                background_tile = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(self.screen, colour, background_tile)

        # Draw vertical grid lines
        for x in range(0, self.WINDOW_WIDTH, self.tile_size):
            pygame.draw.line(self.screen, self.border, (x, 0), (x, self.WINDOW_HEIGHT))
        # Draw horizontal grid lines
        for y in range(0, self.WINDOW_HEIGHT, self.tile_size):
            pygame.draw.line(self.screen, self.border, (0, y), (self.WINDOW_WIDTH, y))

    def drawPlayer(self, player_x, player_y):
        player_rect = pygame.Rect(
            player_x * self.tile_size,
            player_y * self.tile_size,
            self.tile_size,
            self.tile_size,
        )
        pygame.draw.rect(self.self.screen, self.player_colour, player_rect)

    def snapCoordinates(self, x, y):
        factor_x = round(x / self.tile_size)
        factor_y = round(y / self.tile_size)

        factor_x *= self.tile_size
        factor_y *= self.tile_size

        return (factor_x, factor_y)

    def pixel_to_grid(self, px, py):
        return px // self.tile_size, py // self.tile_size
