import sys
import pygame

from settings import Settings


def run_game():
    # 初始化游戏并创建游戏窗口
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # 开始游戏主循环
    while True:

        '''监视鼠标和键盘'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(ai_settings.bg_color)
        pygame.display.flip()


run_game()
