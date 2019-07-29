import pygame
import sys
from time import sleep

from bullet import Bullet
from aliens import Alien


def keydown(event, ship, screen, ai_settings, bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_UP:
        ship.move_up = True
    elif event.key == pygame.K_DOWN:
        ship.move_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, ship, screen)
    elif event.key == pygame.K_q:
        sys.exit()


def keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False
    if event.key == pygame.K_UP:
        ship.move_up = False
    if event.key == pygame.K_DOWN:
        ship.move_down = False


'''检查事件，例如退出游戏，按键'''


def check_events(ship, screen, ai_settings, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown(event, ship, screen, ai_settings, bullets)
        elif event.type == pygame.KEYUP:
            keyup(event, ship)


def update_screen(screen, ai_settings, ship, bullets, aliens):
    screen.fill(ai_settings.bg_color)
    ship.blitme()  # 描绘飞船
    aliens.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()


def update_bullets(aliens, bullets, ai_settings, screen, ship):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    '''检查碰撞'''
    check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship)


def check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)


def fire_bullet(bullets, ai_settings, ship, screen):
    if len(bullets) < ai_settings.bullets_allow:
        for i in range(2):
            new_bullet = Bullet(ship, screen, ai_settings)
            new_bullet.y += i * (ai_settings.bullet_height + 3)
            bullets.add(new_bullet)


'''创建外星人队'''


def get_number_aliens_x(ai_settings, screen):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    return int(
        (ai_settings.screen_width - 2 * alien_width) / (2 * alien_width))


def get_number_aliens_row(ai_settings, screen, ship_height):
    alien = Alien(ai_settings, screen)
    alien_height = alien.rect.height
    return int((ai_settings.screen_height - 3 *
                alien_height - ship_height) / (2 * alien_height))


def creat_alien(
        number_aliens_x,
        number_aliens_row,
        ai_settings,
        screen,
        aliens):
    for row in range(number_aliens_row):
        for number in range(number_aliens_x - 1):
            alien = Alien(ai_settings, screen)
            alien_width = alien.rect.width
            alien.x = alien_width + 2 * alien_width * number
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
            alien.rect.x = alien.x
            aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    number_aliens_x = get_number_aliens_x(ai_settings, screen)
    number_aliens_row = get_number_aliens_row(
        ai_settings, screen, ship_height=ship.rect.height)
    creat_alien(
        number_aliens_x,
        number_aliens_row,
        ai_settings,
        screen,
        aliens)


def aliens_update(ai_settings, aliens, ship, stats, screen, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom - 2:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens:
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
