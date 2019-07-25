import pygame

from settings import Settings
from ship import Ship
import game_func as gf


def run_game():
    # 初始化游戏并创建游戏窗口
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    ship = Ship(screen, ai_settings)  # 创建飞船

    # 开始游戏主循环
    while True:
        '''监视鼠标和键盘'''
        gf.check_events(ship)
        ship.update()
        gf.update_screen(screen, ai_settings, ship)


run_game()
