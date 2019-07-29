import pygame
from pygame.sprite import Group


from settings import Settings
from ship import Ship
import game_func as gf
from game_stats import GameStats


def run_game():
    # 初始化游戏并创建游戏窗口
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    ship = Ship(screen, ai_settings)  # 创建飞船
    aliens = Group()  # 创建外星人
    bullets = Group()
    stats = GameStats(ai_settings)

    gf.create_fleet(ai_settings, screen, aliens, ship)

    # 开始游戏主循环
    while True:
        '''监视鼠标和键盘'''
        gf.check_events(ship, screen, ai_settings, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(aliens, bullets, ai_settings, screen, ship)
            gf.aliens_update(ai_settings, aliens, ship, stats, screen, bullets)
        gf.update_screen(screen, ai_settings, ship, bullets, aliens)


run_game()
