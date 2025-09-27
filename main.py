import pygame
from draw_logic import *
from player import *

import enum

pygame.init()


running = True

while running:
    drawGrid()
    drawPlayer(player_x, player_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            snapped = pixel_to_grid(mouse_x, mouse_y)
            player_x, player_y = snapped

    pygame.display.flip()
    dt = CLOCK.tick(60) / 1000

pygame.quit()
