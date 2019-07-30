import pygame
from pygame.sprite import Group


from settings import Settings
from ship import Ship
import game_func as gf
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # 初始化游戏并创建游戏窗口
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("back_music.mp3")
    pygame.mixer.music.set_volume(0.5)

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption(' Alien Invasion')

    play_button = Button(ai_settings, screen, 'Play')

    ship = Ship(screen, ai_settings)  # 创建飞船
    aliens = Group()  # 创建外星人
    bullets = Group()  # 创建子弹
    stats = GameStats(ai_settings)
    scoreboard = ScoreBoard(ai_settings, screen, stats)

    gf.create_fleet(ai_settings, screen, aliens, ship)

    # 开始游戏主循环
    while True:
        '''监视鼠标和键盘'''
        gf.high_score_memory(stats)
        gf.check_events(
            ship,
            screen,
            ai_settings,
            bullets,
            stats,
            play_button,
            aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(
                aliens,
                bullets,
                ai_settings,
                screen,
                ship,
                stats,
                scoreboard)
            gf.aliens_update(
                ai_settings,
                aliens,
                ship,
                stats,
                screen,
                bullets,
                scoreboard)
        gf.update_screen(
            screen,
            ai_settings,
            ship,
            bullets,
            aliens,
            stats,
            play_button,
            scoreboard)


run_game()
