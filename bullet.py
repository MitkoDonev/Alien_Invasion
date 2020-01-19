import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # a class to manage bullets fired from the ship
    def __init__(self, ai_game):
        # create a bullet object at ships current position
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.settings
        self.color = self.setting.bullet_color

        # create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                                self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # sore the bullets positions as a decimal
        self.y = float(self.rect.y)

    def update(self):
        # move the bullets up the screen
        # update decimal position of the bullet
        self.y -= self.setting.bullet_speed
        # update the position
        self.rect.y = self.y

    def draw_bullet(self):
        # draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)
