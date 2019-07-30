class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ships_limit = 3
        self.fleet_drop_speed = 10

        # 子弹的属性
        self.bullet_width = 4
        self.bullet_height = 12
        self.bullet_color = (60, 60, 60)
        self.bullets_allow = 4

        self.speed_scale = 1.1
        self.initialize_dynameic_settings()

        self.alien_points = 50
        self.score_scale = 1.5

    def initialize_dynameic_settings(self):
        self.ship_speed = 1.5
        self.alien_speed = 2
        self.bullet_speed = 3
        self.fleet_direction = 1


    def increase_speed(self):
        self.ship_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.alien_points = int(self.alien_points * self.score_scale)