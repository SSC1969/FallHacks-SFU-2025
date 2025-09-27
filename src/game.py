import pygame

from src.draw_logic import DrawLogic
from src.player import Player

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TREE_PANEL_WIDTH_RATIO = 0.382
GRID_BORDER = (200, 200, 200)
PLAYER_COLOUR = (255, 0, 128)

LEVEL_ONE = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 3, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 2],
    [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 2, 1, 1, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2],
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1],
]


class Game:
    """Game class to be used globally across modules to sync
    window/clock/other information"""

    window: object
    tree_screen: object
    world_screen: object
    clock: object
    draw_logic: object
    player: Player
    running = False

    def __init__(self):
        """Game initialization"""
        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tree_screen = pygame.Surface(
            (TREE_PANEL_WIDTH_RATIO * WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.world_screen = pygame.Surface(
            ((1 - TREE_PANEL_WIDTH_RATIO) * WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.draw_logic = DrawLogic(
            self.world_screen,
            (self.world_screen.get_width(), WINDOW_HEIGHT),
            GRID_BORDER,
            PLAYER_COLOUR,
        )
        self.draw_logic.level = LEVEL_ONE

        self.player = Player(5, 5)
        self.player.level = LEVEL_ONE

        self.running = True

    def processInput(self):
        """Contains any input checks and the functions they call"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # NOTE: Temporary input functions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.player.moveRight()
                elif event.key == pygame.K_s:
                    self.player.moveDown()
                elif event.key == pygame.K_a:
                    self.player.moveLeft()
                elif event.key == pygame.K_w:
                    self.player.moveUp()

    def update(self):
        """Contains functions that are run each frame to update the game state"""
        if self.player.dead:
            self.running = False
        pass

    def render(self):
        """Contains functions that render the current game state"""
        self.window.fill("black")
        self.tree_screen.fill("gray")
        self.world_screen.fill("red")

        self.draw_logic.drawGrid()
        self.draw_logic.drawPlayer(self.player)

        self.window.blit(self.tree_screen, (0, 0))
        self.window.blit(self.world_screen, (TREE_PANEL_WIDTH_RATIO * WINDOW_WIDTH, 0))
        pygame.display.update()

    def run(self):
        """The main loop of the game"""
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)
