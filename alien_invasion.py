import sys
import pygame


def run_game():
    # 初始化游戏并创建游戏窗口
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Alien Invasion')
    bg_color = (200, 200, 200)

    # 开始游戏主循环
    while True:

        '''监视鼠标和键盘'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(bg_color)
        pygame.display.flip()


run_game()

