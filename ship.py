import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    # a class the manage the ship

    def __init__(self, ai_game):
        # initialize the ship and its starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load the ship image and its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # each new ship start at the bottom of the screen and in the center
        self.rect.midbottom = self.screen_rect.midbottom

        # store a decimal value for the ship's horizotal positiom
        self.x = float(self.rect.x)

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        # update the ship's position, based on the flag
        # update the ship's value, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        # draw the ship at its current position
        self.screen.blit(self.image, self.rect)

    def centre_ship(self):
        # centre ship in centre of screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
