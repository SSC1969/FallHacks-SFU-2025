import pygame

from src.draw_logic import DrawLogic

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TREE_PANEL_WIDTH_RATIO = 0.382
GRID_BORDER = (200, 200, 200)
PLAYER_COLOUR = (255, 0, 128)


class Game:
    """Game class to be used globally across modules to sync
    window/clock/other information"""

    window: object
    tree_screen: object
    world_screen: object
    clock: object
    draw_logic: object
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
        self.running = True

    def processInput(self):
        """Contains any input checks and the functions they call"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Contains functions that are run each frame to update the game state"""
        pass

    def render(self):
        """Contains functions that render the current game state"""
        self.window.fill("black")
        self.tree_screen.fill("gray")
        self.world_screen.fill("red")

        self.draw_logic.drawGrid()
        self.draw_logic.drawPlayer(5, 5)

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
