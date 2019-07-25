import pygame


class Ship:
    def __init__(self, screen, ai_settings):
        """初始化飞船的位置"""
        self.screen = screen
        self.move_right = False
        self.move_left = False
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        '''将飞船放在底部中央'''
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.move_left and self.rect.centerx > 0:
            self.center -= self.ai_settings.ship_speed
        if self.move_right and self.rect.centerx < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed

        self.rect.centerx = self.center
