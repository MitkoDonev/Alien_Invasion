import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    # Class to manage game assets and behavior
    def __init__(self):
        # initialize the game and create game resources
        pygame.init()
        self.settings = Settings()

        # windowed
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # create instance of scoreboard
        # create instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # create play button
        self.play_button = Button(self, 'Play')

    def _create_fleet(self):
        # create the fleet of aliens
        # make an alien object and find the number of aliens in a row
        # spacing in equal to one alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = available_space_x // (2 * alien_width)

        # determine the number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # create the first row of aliens
        # create a full screen of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # create the first row of aliens
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def run_game(self):
        # start loop for main game
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # check for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # move the ship to the right
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # start new game when player clicks play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # reset game stats
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # remove remaining aliens
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and centre ship

            self._create_fleet()
            self.ship.centre_ship()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        # respond to key press
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # create a new bullet amd add ot to tje bullet group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update position of bullets and remove old bullets
        # update bullet position
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        # respond to alien - bullet collision
        # remove bullet and aliens that have collided
        # check if bullet hit target
        # if yes, remove alien and bullet
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            # destroy existing bullets amd create ew fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_fleet_edges(self):
        # respond if any alien has reached the edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # change the fleet direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        # check if the fleet is on edge and update
        self._check_fleet_edges()
        # update the position of aliens
        self.aliens.update()

        # look fpr alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for alien reaching the bottom
        self._check_aliens_bottom()

    def _ship_hit(self):
        # respond to ship being hit by alien
        if self.stats.ships_left > 1:
            # decrement ship_limit
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # remove any left aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and centre ship
            self._create_fleet()
            self.ship.centre_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        # check if alien reached the bottom
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # treat as if ship is hit
                self._ship_hit()
                break

    def _update_screen(self):
        # redraw the screen during each pass through the loop
        self.screen.fill(self.settings.screen_bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draw scoreboard information
        self.sb.show_score()

        # draw play button, if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make most recent drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # make a game instance and run game
    ai = AlienInvasion()
    ai.run_game()
