import pygame
from draw_logic import *
from player import *

import enum

pygame.init()

from src.game import Game

game = Game()
game.run()


character = player(0, 0)
# starts at 0, 0
all_sprites = pygame.sprite.Group(character)

running = True
winCondition = False

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: character.moveUp()
            elif event.key == pygame.K_DOWN: character.moveDown()
            elif event.key == pygame.K_LEFT: character.moveLeft()
            elif event.key == pygame.K_RIGHT: character.moveRight()
    
    all_sprites.draw(SCREEN)

    pygame.display.flip()
    dt = CLOCK.tick(60) / 1000

pygame.quit()
