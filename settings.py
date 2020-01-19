class Settings:
    # a class to store all settings for Alien Invasion

    def __init__(self):
        # initialize the game settings
        # screen settings
        self.screen_width = 1200
        # 1366
        self.screen_height = 600
        # 768
        self.screen_bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        # original bullet speed is 1.5
        self.bullet_width = 3
        self.bullet_height = 8
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        # how quick the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # ship settings
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet direction of 1 represents tight; -1 represents left
        self.fleet_direction = 1

        # scoring
        self.alien_points = 20

    def increase_speed(self):
        # increase speed settings
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
