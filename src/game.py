import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


class Game:
    window: object
    clock: object
    running = False

    def __init__(self):
        """Game initialization"""
        pygame.init()

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        """Contains any input checks and the functions they call"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pass

    def update(self):
        """Contains functions that are run each frame to update the game state"""
        pass

    def render(self):
        """Contains functions that render the current game state"""
        self.window.fill("black")
        pygame.display.update()

    def run(self):
        """The main loop of the game"""
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)
