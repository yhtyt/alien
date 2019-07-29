class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.ships_limit = 3

        self.alien_speed = 1
        self.fleet_drop_speed = 5
        self.fleet_direction = 1

        # 子弹的属性
        self.bullet_speed = 3
        self.bullet_width = 4
        self.bullet_height = 12
        self.bullet_color = (60, 60, 60)

        self.bullets_allow = 6
