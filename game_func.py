import pygame
import sys
from time import sleep
import threading
import json

from bullet import Bullet
from aliens import Alien


def high_score_memory(stats):
    filename = 'high_score.json'
    if stats.high_score > 0:
        with open(filename, 'w') as high:
            json.dump(stats.high_score, high)
    with open(filename) as read:
        stats.high_score = json.load(read)


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
        t = threading.Thread(target=play_sound('images/bullet.wav'))
        t.start()
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


def check_play_button(
        stats,
        play_button,
        mouse_x,
        mouse_y,
        aliens,
        bullets,
        ship,
        screen,
        ai_settings):
    if play_button.rect.collidepoint(
            mouse_x, mouse_y) and not stats.game_active:

        stats.game_active = True  # 若鼠标点击开始游戏

        play_button.prep_msg('Play Again')

        aliens.empty()
        bullets.empty()
        ai_settings.initialize_dynameic_settings()  # 初始化设置
        stats.reset_stats()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        pygame.mouse.set_visible(False)  # 隐藏鼠标

        pygame.mixer.music.play(-1)  # 播放背景音乐


def check_high_score(scoreboard, stats):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
    scoreboard.prep_high_score()


'''检查事件，例如退出游戏，按键'''


def check_events(
        ship,
        screen,
        ai_settings,
        bullets,
        stats,
        play_button,
        aliens):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keydown(event, ship, screen, ai_settings, bullets)
        elif event.type == pygame.KEYUP:
            keyup(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                stats,
                play_button,
                mouse_x,
                mouse_y,
                aliens,
                bullets,
                ship,
                screen,
                ai_settings)


def update_screen(
        screen,
        ai_settings,
        ship,
        bullets,
        aliens,
        stats,
        play_button,
        scoreboard):
    screen.fill(ai_settings.bg_color)

    scoreboard.prep_high_score()
    scoreboard.prep_ship()
    scoreboard.show_score()

    ship.blitme()  # 描绘飞船
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.display.flip()


def update_bullets(
        aliens,
        bullets,
        ai_settings,
        screen,
        ship,
        stats,
        scoreboard):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    '''检查碰撞'''
    check_bullet_alien_collision(
        bullets,
        aliens,
        ai_settings,
        screen,
        ship,
        stats,
        scoreboard)


def check_bullet_alien_collision(
        bullets,
        aliens,
        ai_settings,
        screen,
        ship,
        stats,
        scoreboard):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(collisions):
        t = threading.Thread(target=play_sound('images/collision.wav'))
        t.start()
        for alien in collisions.values():
            stats.score += ai_settings.alien_points
            scoreboard.prep_score()

    if len(aliens) == 0:
        bullets.empty()
        stats.level += 1
        scoreboard.prep_level()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)

    check_high_score(scoreboard, stats)
    scoreboard.prep_score()
    scoreboard.prep_level()


def fire_bullet(bullets, ai_settings, ship, screen):
    if len(bullets) < ai_settings.bullets_allow:
        new_bullet = Bullet(ship, screen, ai_settings)
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


def aliens_update(
        ai_settings,
        aliens,
        ship,
        stats,
        screen,
        bullets,
        scoreboard):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
    check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)


def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom - 2:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard)
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


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, scoreboard):
    if stats.ships_left > 1:
        stats.ships_left -= 1
        scoreboard.prep_ship()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

        pygame.mixer.music.pause()
        t = threading.Thread(target=play_sound('images/game_over.wav'))
        t.start()


def play_sound(path):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(0.3)
    if path == 'images/bullet.wav':
        sound.play(1, 635)
    elif path == 'images/collision.wav':
        sound.play(1, 1100)
    else:
        sound.play(1, int(sound.get_length() * 1000))
