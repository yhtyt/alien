import pygame
import sys


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def update_screen(screen, ai_settings, ship):
    screen.fill(ai_settings.bg_color)
    ship.blitme()  # 描绘飞船
    pygame.display.flip()

