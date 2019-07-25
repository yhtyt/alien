import pygame
import sys


def keydown(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True


def keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False


def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown(event, ship)
        elif event.type == pygame.KEYUP:
            keyup(event, ship)


def update_screen(screen, ai_settings, ship):
    screen.fill(ai_settings.bg_color)
    ship.blitme()  # 描绘飞船
    pygame.display.flip()
