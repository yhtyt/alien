import pygame
import sys
from bullet import Bullet


def keydown(event, ship, screen, ai_settings, bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fir_bullet(bullets, ai_settings, ship, screen)


def keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False


'''检查事件，例如退出游戏，按键'''


def check_events(ship, screen, ai_settings, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown(event, ship, screen, ai_settings, bullets)
        elif event.type == pygame.KEYUP:
            keyup(event, ship)


def update_screen(screen, ai_settings, ship, bullets):
    screen.fill(ai_settings.bg_color)
    ship.blitme()  # 描绘飞船
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()


def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fir_bullet(bullets, ai_settings, ship, screen):
    if len(bullets) < ai_settings.bullets_allow:
        for i in range(2):
            new_bullet = Bullet(ship, screen, ai_settings)
            new_bullet.y += i * (ai_settings.bullet_height + 3)
            bullets.add(new_bullet)
